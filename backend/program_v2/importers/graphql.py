import logging
from datetime import timedelta

import requests

from core.models.event import Event
from dimensions.models.dimension_dto import DimensionDTO, DimensionValueDTO

from ..models.program import Program
from ..models.program_dimension_value import ProgramDimensionValue
from ..models.schedule import ScheduleItem

logger = logging.getLogger("kompassi")
IMPORT_QUERY = """
query ImportProgram($eventSlug: String!, $lang: String!) {
  event(slug: $eventSlug) {
    program {
      dimensions {
        slug
        title(lang: $lang)
        values {
          slug
          title(lang: $lang)
        }
      }
      programs {
        slug
        title
        description
        annotations
        cachedDimensions
        scheduleItems {
          slug
          subtitle
          startTime
          lengthMinutes
        }
      }
    }
  }
}
"""


def import_graphql(
    event: Event,
    graphql_url: str = "https://kompassi.eu/graphql",
    language: str = "fi",
) -> None:
    """
    Import program data from GraphQL API.

    :param event_slug: Slug of the event to import program data to.
    :param base_url: Base URL of the GraphQL API.

    TODO multiple languages
    """

    response = requests.post(
        graphql_url,
        json=dict(
            query=IMPORT_QUERY,
            variables=dict(
                eventSlug=event.slug,
                lang=language,
            ),
        ),
    )

    try:
        response.raise_for_status()
    except requests.HTTPError:
        logger.error("GraphQL error while fetching program data for %s: %s", event.slug, response.json())
        raise

    data = response.json()

    dimensions = DimensionDTO.save_many(
        event.program_universe,
        [
            DimensionDTO(
                slug=dimension_data["slug"],
                title={language: dimension_data["title"]},
                choices=[
                    DimensionValueDTO(
                        slug=value_data["slug"],
                        title={language: value_data["title"]},
                    )
                    for value_data in dimension_data["values"]
                ],
            )
            for dimension_data in data["data"]["event"]["program"]["dimensions"]
        ],
    )
    logger.info("Imported %d dimensions for %s", len(dimensions), event.slug)

    programs = Program.objects.bulk_create(
        [
            Program(
                event=event,
                slug=program_data["slug"],
                title=program_data["title"],
                description=program_data["description"],
                annotations=program_data["annotations"],
            )
            for program_data in data["data"]["event"]["program"]["programs"]
        ],
        update_conflicts=True,
        unique_fields=["event", "slug"],
        update_fields=["title", "description", "annotations", "updated_at"],
    )
    logger.info("Imported %d programs for %s", len(programs), event.slug)

    ScheduleItem.objects.filter(program__in=programs).delete()
    schedule_items = ScheduleItem.objects.bulk_create(
        [
            ScheduleItem(
                program=program,
                slug=schedule_item["slug"],
                subtitle=schedule_item["subtitle"],
                start_time=schedule_item["startTime"],
                length=timedelta(minutes=schedule_item["lengthMinutes"]),
            ).with_generated_fields()
            for program, program_data in zip(programs, data["data"]["event"]["program"]["programs"], strict=True)
            for schedule_item in program_data["scheduleItems"]
        ]
    )
    logger.info("Imported %d schedule items for %s", len(schedule_items), event.slug)

    upsert_cache = ProgramDimensionValue.build_upsert_cache(event)
    pdv_upsert = [
        item
        for program, program_data in zip(programs, data["data"]["event"]["program"]["programs"], strict=True)
        for item in ProgramDimensionValue.build_upsertables(
            program,
            program_data["cachedDimensions"],
            upsert_cache,
        )
    ]
    pdvs = ProgramDimensionValue.bulk_upsert(pdv_upsert)
    logger.info("Imported %d program dimension values for %s", len(pdvs), event.slug)

    pdv_ids = {pdv.id for pdv in pdvs}
    ProgramDimensionValue.objects.filter(program__in=programs).exclude(id__in=pdv_ids).delete()

    Program.refresh_cached_fields_qs(event.programs.all())
