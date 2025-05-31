import logging
from collections.abc import Iterable, Sequence
from datetime import timedelta
from typing import ClassVar

from core.models.event import Event
from dimensions.models.dimension import Dimension
from dimensions.models.dimension_dto import DimensionDTO, DimensionValueDTO, ValueOrdering
from dimensions.models.universe import Universe
from forms.models.enums import Anonymity, SurveyApp, SurveyPurpose
from forms.models.response import Response
from forms.models.survey import Survey
from forms.models.workflow import Workflow
from graphql_api.language import SUPPORTED_LANGUAGE_CODES
from involvement.models.involvement import Involvement
from tickets_v2.views.pos_view import HttpRequest

from ..models.program import Program

logger = logging.getLogger("kompassi")

DATE_DIMENSION_TITLE_LOCALIZED = dict(
    fi="Päivä",
    en="Day",
    sv="Dag",
)

ROOM_DIMENSION_DTO = DimensionDTO(
    slug="room",
    value_ordering=ValueOrdering.TITLE,
    is_public=True,
    is_list_filter=True,
    is_key_dimension=False,
    is_technical=True,  # but the values are not
    title=dict(
        fi="Sali",
        en="Room",
        sv="Sal",
    ),
)

WEEKDAYS_LOCALIZED = dict(
    fi=["maanantai", "tiistai", "keskiviikko", "torstai", "perjantai", "lauantai", "sunnuntai"],
    en=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
    sv=["måndag", "tisdag", "onsdag", "torsdag", "fredag", "lördag", "söndag"],
)


STATE_DIMENSION_DTO = DimensionDTO(
    slug="state",
    value_ordering=ValueOrdering.MANUAL,
    is_public=False,
    is_list_filter=True,
    is_key_dimension=True,
    is_technical=True,
    title={
        "fi": "Tila",
        "en": "State",
        "sv": "Status",
    },
    choices=[
        DimensionValueDTO(
            slug="new",
            is_technical=True,
            title={
                "fi": "Uusi",
                "en": "New",
                "sv": "Nytt",
            },
            color="Blue",
        ),
        DimensionValueDTO(
            slug="accepted",
            is_technical=True,
            # cannot use is_subject_locked on state=accepted because
            # we may want to allow editing the program but not the offer
            title={
                "fi": "Hyväksytty",
                "en": "Accepted",
                "sv": "Godkänt",
            },
            color="Green",
        ),
        DimensionValueDTO(
            slug="rejected",
            is_technical=True,
            is_subject_locked=True,
            title={
                "fi": "Hylätty",
                "en": "Rejected",
                "sv": "Avvisad",
            },
            color="Red",
        ),
        DimensionValueDTO(
            slug="cancelled",
            is_technical=True,
            is_subject_locked=True,
            title={
                "fi": "Peruutettu",
                "en": "Cancelled",
                "sv": "Avbruten",
            },
            color="Red",
        ),
    ],
)


class ProgramOfferWorkflow(Workflow, arbitrary_types_allowed=True):
    """
    Survey response workflow for the program offer to program item pipeline.
    """

    survey: Survey

    @classmethod
    def get_program_universe(cls, event: Event) -> Universe:
        """
        Returns the universe for the program offer workflow.
        """
        universe, created = Universe.objects.get_or_create(
            scope=event.scope,
            slug="program",
            app="program_v2",
        )

        if created:
            cls._setup_default_dimensions(universe)

        return universe

    @classmethod
    def _get_default_dimension_values(cls, survey: Survey) -> dict[str, list[str]]:
        return {
            "state": ["new"],
            "form": [survey.slug],
        }

    def handle_new_survey(self):
        super().handle_new_survey()
        self._setup_default_dimensions(self.survey.universe)
        self.survey.set_default_dimension_values(
            self._get_default_dimension_values(self.survey),
            self.survey.universe.preload_dimensions(),
        )

    @classmethod
    def backfill(cls, event: Event):
        logger.info("Backfilling program V2 settings for event %s", event.slug)

        program_universe = cls.get_program_universe(event)
        cls._setup_default_dimensions(program_universe)
        program_cache = program_universe.preload_dimensions()

        meta = event.program_v2_event_meta
        if meta is None:
            raise ValueError("Event has no program_v2_event_meta")

        if not meta.default_registry:
            raise ValueError("Event has no default registry for program_v2")

        # Program form settings
        Survey.objects.filter(
            event=event,
            app="program_v2",
        ).update(
            anonymity=Anonymity.FULL_PROFILE.value,
            registry=meta.default_registry,
        )

        for offer_form in meta.program_offer_forms.all():
            offer_form.with_mandatory_attributes_for_app(SurveyApp.PROGRAM_V2, SurveyPurpose.DEFAULT).save()
            offer_form.set_default_dimension_values(cls._get_default_dimension_values(offer_form), program_cache)

        # Program offer dimensions
        for program_offer in meta.current_program_offers.all():
            existing_values = program_offer.cached_dimensions
            values_to_set = {}

            if not existing_values.get("state", []):
                values_to_set["state"] = ["accepted"] if program_offer.programs.exists() else ["new"]
            if not existing_values.get("form", []):
                values_to_set["form"] = [program_offer.survey.slug]

            if values_to_set:
                program_offer.set_dimension_values(values_to_set, program_cache)

        # Program dimensions
        for program in Program.objects.filter(event=event):
            existing_values = program.cached_dimensions
            values_to_set = {}

            if not existing_values.get("state", []):
                values_to_set["state"] = ["accepted"]
            if not existing_values.get("form", []):
                values_to_set["form"] = [program.program_offer.survey.slug] if program.program_offer else []

            if values_to_set:
                program.set_dimension_values(values_to_set, program_cache)

        Program.refresh_cached_fields_qs(Program.objects.filter(event=event))

        # Involvements
        involvement_universe = event.involvement_universe
        Involvement.setup_dimensions(involvement_universe)
        involvement_cache = involvement_universe.preload_dimensions()

        for program_offer in Response.objects.filter(
            form__event=event,
            form__survey__app="program_v2",
            superseded_by=None,
        ):
            program_offer.survey.workflow.ensure_involvement(program_offer, cache=involvement_cache)

        for program in Program.objects.filter(event=event, program_offer__isnull=False):
            Involvement.from_accepted_program_offer(
                program_offer=program.program_offer,
                program=program,
                cache=involvement_cache,
            )

        Program.refresh_cached_fields_qs(Program.objects.filter(event=event))

    def handle_form_update(self):
        """
        If form titles have changed, update them in the dimension.
        """
        universe = self.survey.universe
        self._get_form_dimension_dto(universe).save(universe)

    @classmethod
    def _setup_default_dimensions(cls, universe: Universe) -> Sequence[Dimension]:
        return DimensionDTO.save_many(
            universe,
            [
                cls._get_date_dimension_dto(universe),
                ROOM_DIMENSION_DTO,
                cls._get_form_dimension_dto(universe),
                STATE_DIMENSION_DTO,
            ],
        )

    @classmethod
    def _get_form_dimension_dto(cls, universe: Universe) -> DimensionDTO:
        """
        We make the form used to submit a program offer a dimension
        in order to not have to build separate filters for it.
        """
        event: Event = universe.scope.event
        if not event:
            raise ValueError("Event is not set for universe")

        meta = event.program_v2_event_meta
        if meta is None:
            raise ValueError("Event has no program_v2_event_meta")

        return DimensionDTO(
            slug="form",
            value_ordering=ValueOrdering.TITLE,
            is_public=False,
            is_list_filter=True,
            is_key_dimension=True,
            is_technical=True,
            title={
                "fi": "Ohjelmalomake",
                "en": "Program form",
                "sv": "Programblankett",
            },
            choices=[
                DimensionValueDTO(
                    slug=survey.slug,
                    is_technical=True,
                    title=survey.title_dict,
                )
                for survey in meta.program_offer_forms.only("id", "slug")
            ],
        )

    date_cutoff_time: ClassVar[timedelta] = timedelta(hours=4)  # 04:00 local time

    def _get_date_dimension_value(self, program: Program) -> list[str]:
        """
        Return the date dimension value for the programme.

        The `date_cutoff_time` is used to determine at which time of the night the date changes.
        Use this to make the wee hours of the night belong to the previous day.
        """
        tz = self.survey.event.timezone
        return [
            (sitem.start_time.astimezone(tz) - self.date_cutoff_time).date().isoformat()
            for sitem in program.schedule_items.all()
        ]

    @classmethod
    def _get_date_dimension_values(cls, universe: Universe) -> Iterable[DimensionValueDTO]:
        """
        Return a list of DimensionValueDTOs for the date dimension.
        """
        event: Event = universe.scope.event
        tz = event.timezone

        if not event.start_time:
            raise ValueError(f"Event {event} has no start time")
        if not event.end_time:
            raise ValueError(f"Event {event} has no end time")

        cur_date = event.start_time.astimezone(tz).date()
        end_date = event.end_time.astimezone(tz).date()

        while cur_date <= end_date:
            yield DimensionValueDTO(
                slug=cur_date.isoformat(),
                title={
                    lang_code: WEEKDAYS_LOCALIZED[lang_code][cur_date.weekday()]
                    for lang_code in SUPPORTED_LANGUAGE_CODES
                },
                is_technical=True,
            )
            cur_date += timedelta(days=1)

    @classmethod
    def _get_date_dimension_dto(cls, universe: Universe) -> DimensionDTO:
        """
        Reusable date dimension for importers that define their own dimensions in `get_dimensions`.
        """
        return DimensionDTO(
            slug="date",
            title=DATE_DIMENSION_TITLE_LOCALIZED,
            choices=list(cls._get_date_dimension_values(universe)),
            value_ordering=ValueOrdering.SLUG,
            is_public=True,
            is_list_filter=True,
            is_technical=True,
        )

    def is_response_active(self, response: Response) -> bool:
        return not bool(set(response.cached_dimensions.get("state", [])).intersection({"cancelled", "rejected"}))

    def ensure_survey_to_badge(self, response: Response):
        """
        The program offer workflow doesn't use STB.
        Badges are managed via Involvement.
        """
        return None, False

    def response_can_be_edited_by(self, response: Response, request: HttpRequest) -> bool:
        # cannot use is_subject_locked on state=accepted because we may want to allow editing the program but not the offer
        return super().response_can_be_edited_by(response, request) and "new" in response.cached_dimensions.get(
            "state", ["new"]
        )
