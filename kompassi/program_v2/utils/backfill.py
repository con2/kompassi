import logging

from django.db import transaction

from kompassi.core.models.event import Event
from kompassi.core.utils.log_utils import log_get_or_create
from kompassi.dimensions.models.enums import DimensionApp
from kompassi.forms.models.enums import Anonymity
from kompassi.forms.models.survey import Survey
from kompassi.involvement.dimensions import setup_involvement_dimensions
from kompassi.involvement.models.involvement import Involvement
from kompassi.involvement.models.meta import InvolvementEventMeta
from kompassi.involvement.models.registry import Registry

from ..dimensions import get_program_universe, setup_program_dimensions
from ..models.program import Program
from ..models.schedule_item import ScheduleItem
from ..workflows.program_offer import ProgramOfferWorkflow

logger = logging.getLogger(__name__)


def backfill(
    event: Event,
    override_involvement_dimensions: bool = False,
):
    """
    New technical dimensions and dimension default value handling has been introduced
    during the development of Program V2. This method backfills the existing
    program offers and programs with the new dimensions and default values.

    :param override_involvement_dimensions:
        If True, each program host will receive the default involvement dimensions
        of the form that they used to become a program host.
    """

    logger.info(
        "Backfilling program V2 settings for event %s. Note that this may take several minutes for a large event.",
        event.slug,
    )

    meta = event.program_v2_event_meta
    if meta is None:
        raise ValueError("Event has no program_v2_event_meta")

    if not meta.default_registry:
        meta.default_registry, created = Registry.objects.get_or_create(
            scope=event.organization.scope,
            slug="volunteers",
            defaults=dict(
                title_fi=f"{event.organization.name} -vapaaehtoisrekisteri",
                title_en=f"Volunteers of {event.organization.name}",
            ),
        )
        log_get_or_create(logger, meta.default_registry, created)

    with transaction.atomic():
        program_universe = get_program_universe(event)
        setup_program_dimensions(program_universe)
        program_cache = program_universe.preload_dimensions()

    # Program form settings
    Survey.objects.filter(
        event=event,
        app_name=DimensionApp.PROGRAM_V2.value,
    ).update(
        anonymity=Anonymity.FULL_PROFILE.value,
        registry=meta.default_registry,
    )

    with transaction.atomic():
        for offer_form in meta.program_offer_forms.all():
            offer_form.with_mandatory_fields().save()
            offer_form.set_default_response_dimension_values(
                ProgramOfferWorkflow._get_default_dimension_values(offer_form),
                cache=program_cache,
            )
            offer_form.refresh_cached_default_dimensions()

    # Program offer dimensions
    with transaction.atomic():
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
    with transaction.atomic():
        for program in Program.objects.filter(event=event):
            existing_values = program.cached_dimensions
            values_to_set = {}

            if not existing_values.get("state", []):
                values_to_set["state"] = ["accepted"]
            if not existing_values.get("form", []):
                values_to_set["form"] = [program.program_offer.survey.slug] if program.program_offer else []

            if values_to_set:
                program.set_dimension_values(values_to_set, program_cache)

    with transaction.atomic():
        Program.refresh_cached_fields_qs(meta.programs.all(), cache=program_cache)
    with transaction.atomic():
        ScheduleItem.refresh_cached_fields_qs(meta.schedule_items.all())

    # Involvements
    InvolvementEventMeta.ensure(event)
    with transaction.atomic():
        involvement_universe = event.involvement_universe
        setup_involvement_dimensions(involvement_universe, event)
        involvement_cache = involvement_universe.preload_dimensions()

    with transaction.atomic():
        logger.info("Backfilling involvement for %d program offers", meta.current_program_offers.count())
        for program_offer in meta.current_program_offers.all():
            program_offer.survey.workflow.ensure_involvement(
                program_offer,
                cache=involvement_cache,
                override_dimensions=override_involvement_dimensions,
            )

    with transaction.atomic():
        logger.info("Backfilling involvement for %d program items", meta.programs.count())
        for program in meta.programs.all():
            for program_host in program.all_program_hosts.all():
                Involvement.from_involvement(
                    involvement=program_host,
                    cache=involvement_cache,
                    override_dimensions=override_involvement_dimensions,
                )

    with transaction.atomic():
        Program.refresh_cached_fields_qs(meta.programs.all(), cache=program_cache)

    logger.info("Backfilling program V2 settings for event %s completed.", event.slug)
