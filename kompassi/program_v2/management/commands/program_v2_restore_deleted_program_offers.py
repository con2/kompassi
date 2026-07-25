import logging

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from kompassi.core.models.event import Event
from kompassi.dimensions.models.enums import DimensionApp
from kompassi.forms.models.enums import SurveyPurpose
from kompassi.forms.models.form import Form
from kompassi.forms.models.response import Response
from kompassi.forms.models.response_dimension_value import ResponseDimensionValue
from kompassi.involvement.models.enums import InvolvementApp, InvolvementType
from kompassi.involvement.models.involvement import Involvement
from kompassi.involvement.models.involvement_dimension_value import InvolvementDimensionValue
from kompassi.program_v2.models.program import Program

logger = logging.getLogger(__name__)

PITR_ALIAS = "pitr"


class Command(BaseCommand):
    # See kompassi/docs/restore-deleted-program-offers.md for the full runbook.
    help = (
        "Restore program offers (and everything that cascaded from their deletion) for one event "
        f"from a PITR side instance wired up as the {PITR_ALIAS!r} database alias. "
        "Runs as a dry run (rolled back) unless --commit is passed."
    )

    def add_arguments(self, parser):
        parser.add_argument("event_slug", metavar="EVENT_SLUG")
        parser.add_argument(
            "--expected-count",
            type=int,
            default=None,
            help=(
                "Abort unless exactly this many forms.Response rows would be restored. "
                "Use this to cross-check against count_deleted in the program_v2.program_offer.deleted "
                "event log entry before committing."
            ),
        )
        parser.add_argument(
            "--commit",
            default=False,
            action="store_true",
            help="Actually commit the restore. Without this flag, the restore is rolled back at the end (dry run).",
        )

    def handle(self, *args, **opts):
        event_slug: str = opts["event_slug"]
        expected_count: int | None = opts["expected_count"]
        commit: bool = opts["commit"]

        if PITR_ALIAS not in settings.DATABASES:
            raise CommandError(
                f"No {PITR_ALIAS!r} database alias configured. Set the PITR_POSTGRES_* environment "
                "variables to point it at the PITR side instance before running this command."
            )

        event = Event.objects.get(slug=event_slug)

        offer_forms = Form.objects.filter(
            survey__event=event,
            survey__app_name=DimensionApp.PROGRAM_V2.value,
            survey__purpose_slug=SurveyPurpose.DEFAULT.value,
        )
        form_ids = set(offer_forms.values_list("id", flat=True))
        pitr_form_ids = set(
            Form.objects.using(PITR_ALIAS)
            .filter(
                survey__event__slug=event_slug,
                survey__app_name=DimensionApp.PROGRAM_V2.value,
                survey__purpose_slug=SurveyPurpose.DEFAULT.value,
            )
            .values_list("id", flat=True)
        )
        if form_ids != pitr_form_ids:
            raise CommandError(
                f"Program offer forms differ between default ({len(form_ids)} forms) and {PITR_ALIAS} "
                f"({len(pitr_form_ids)} forms) for {event_slug}. Forms are never touched by "
                "DeleteProgramOffers, so this is unexpected - investigate before proceeding."
            )

        prod_response_ids = set(Response.objects.filter(form_id__in=form_ids).values_list("id", flat=True))
        pitr_response_ids = set(
            Response.objects.using(PITR_ALIAS).filter(form_id__in=form_ids).values_list("id", flat=True)
        )
        missing_response_ids = pitr_response_ids - prod_response_ids
        extra_response_ids = prod_response_ids - pitr_response_ids

        self.stdout.write(
            f"Responses present on {PITR_ALIAS} but missing on default (to be restored): {len(missing_response_ids)}"
        )
        self.stdout.write(
            f"Responses present on default but not on {PITR_ALIAS} "
            f"(created/edited after the PITR snapshot, left untouched): {len(extra_response_ids)}"
        )

        if not missing_response_ids:
            self.stdout.write("Nothing to restore.")
            return

        if expected_count is not None and len(missing_response_ids) != expected_count:
            raise CommandError(
                f"Expected to restore exactly {expected_count} responses, found {len(missing_response_ids)}. "
                "Refusing to proceed."
            )

        with transaction.atomic():
            self._restore(missing_response_ids)

            if commit:
                self.stdout.write(
                    self.style.SUCCESS(f"Committed restore of {len(missing_response_ids)} program offers.")
                )
            else:
                self.stdout.write(
                    self.style.WARNING("Dry run complete, rolling back (pass --commit to apply for real).")
                )
                transaction.set_rollback(True)

    def _restore(self, response_ids: set):
        # 1. forms.Response. superseded_by is a self-FK, so insert with it nulled out first and
        # patch it in a second pass once every row in this batch exists.
        pitr_responses = list(Response.objects.using(PITR_ALIAS).filter(id__in=response_ids))
        superseded_by = {
            response.id: response.superseded_by_id for response in pitr_responses if response.superseded_by_id
        }
        for response in pitr_responses:
            response.superseded_by_id = None
        Response.objects.bulk_create(pitr_responses)
        self.stdout.write(f"  Restored {len(pitr_responses)} forms.Response rows.")

        for response_id, superseded_by_id in superseded_by.items():
            Response.objects.filter(id=response_id).update(superseded_by_id=superseded_by_id)
        self.stdout.write(f"  Relinked superseded_by on {len(superseded_by)} responses.")

        # 2. forms.ResponseDimensionValue. Its own PK is not referenced anywhere else, so let the
        # database assign fresh ids; only (subject, value) need to match the original state.
        dimension_values = list(ResponseDimensionValue.objects.using(PITR_ALIAS).filter(subject_id__in=response_ids))
        for dimension_value in dimension_values:
            dimension_value.id = None
        ResponseDimensionValue.objects.bulk_create(dimension_values)
        self.stdout.write(f"  Restored {len(dimension_values)} forms.ResponseDimensionValue rows.")

        # 3. involvement.Involvement, PROGRAM_OFFER only. PROGRAM_HOST involvements were detached
        # (response set to NULL) rather than deleted by DeleteProgramOffers, so they are untouched.
        pitr_involvements = list(
            Involvement.objects.using(PITR_ALIAS).filter(
                response_id__in=response_ids,
                app=InvolvementApp.PROGRAM,
                type=InvolvementType.PROGRAM_OFFER,
            )
        )
        Involvement.objects.bulk_create(pitr_involvements)
        involvement_ids = [involvement.id for involvement in pitr_involvements]
        self.stdout.write(f"  Restored {len(pitr_involvements)} involvement.Involvement rows.")

        # 4. involvement.InvolvementDimensionValue, same reasoning as (2).
        involvement_dimension_values = list(
            InvolvementDimensionValue.objects.using(PITR_ALIAS).filter(subject_id__in=involvement_ids)
        )
        for dimension_value in involvement_dimension_values:
            dimension_value.id = None
        InvolvementDimensionValue.objects.bulk_create(involvement_dimension_values)
        self.stdout.write(f"  Restored {len(involvement_dimension_values)} involvement.InvolvementDimensionValue rows.")

        # 5. program_v2.Program.program_offer_id was SET NULL, not deleted. Relink it, but only
        # where it is still NULL in default, in case it was legitimately changed since.
        relinked = 0
        for program in Program.objects.using(PITR_ALIAS).filter(program_offer_id__in=response_ids):
            relinked += Program.objects.filter(id=program.id, program_offer_id__isnull=True).update(
                program_offer_id=program.program_offer_id
            )
        self.stdout.write(f"  Relinked program_offer_id on {relinked} program_v2.Program rows.")

        # 6. Recompute denormalized caches from the now-restored dimension values rather than
        # trusting the (possibly stale) cached_dimensions/cached_key_fields copied from pitr.
        Response.refresh_cached_fields_qs(Response.objects.filter(id__in=response_ids))
        Involvement.refresh_cached_dimensions_qs(Involvement.objects.filter(id__in=involvement_ids))
        self.stdout.write("  Refreshed cached dimensions/key fields on restored responses and involvements.")
