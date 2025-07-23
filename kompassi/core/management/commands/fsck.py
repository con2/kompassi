import argparse
import logging
from collections.abc import Iterable

from django.core.management.base import BaseCommand

from kompassi.core.utils.pkg_resources_compat import resource_string
from kompassi.labour.models.roster import Shift
from kompassi.zombies.programme.models.programme_role import ProgrammeRole

from ...models import Event

logger = logging.getLogger(__name__)
DUPLICATE_PROGRAMME_ROLES_SQL = resource_string(__name__, "sql/duplicate_programme_roles.sql").decode()


class Command(BaseCommand):
    args = ""
    help = "Check data integrity"

    events: Iterable[Event]
    fix: bool

    def add_arguments(self, parser):
        parser.add_argument(
            "--event",
            dest="events",
            nargs="*",
            metavar="SLUG",
            help="Events to process (default all)",
            default=None,
        )
        parser.add_argument(
            "--fix",
            default=False,
            action=argparse.BooleanOptionalAction,
            help="Attempt to fix auto-fixable problems",
        )

    def handle(self, *args, **options):
        self.fix = options["fix"]

        if options["events"]:
            self.events = Event.objects.filter(slug__in=options["events"])
        else:
            self.events = Event.objects.all()

        self.labour_check_shifts()
        self.programme_check_double_roles()

    def labour_check_shifts(self):
        for shift in Shift.objects.filter(signup__event__in=self.events):
            jc = shift.job.job_category
            signup = shift.signup
            if not signup.job_categories_accepted.filter(id=jc.id).exists():
                print(
                    f"{shift.signup.event.slug}: Job category of shift not present in "
                    f"accepted job categories of signup (shift = {shift.id}, jc = {jc.id}, signup = {signup.id})"
                )

                if self.fix:
                    shift.signup.job_categories_accepted.add(jc)

    def programme_check_double_roles(self):
        prs = ProgrammeRole.objects.raw(DUPLICATE_PROGRAMME_ROLES_SQL)
        prs = ProgrammeRole.objects.filter(
            id__in={pr.id for pr in prs},
            programme__category__event__in=self.events,
        ).select_related(
            "person",
            "programme__category__event",
        )

        for pr in prs:
            print(
                f"{pr.programme.category.event.slug}: Duplicate programme roles "
                f"(pr = {pr.id}, programme = {pr.programme_id}, person = {pr.person_id})"
            )

        if self.fix:
            # prs contains only the duplicates due to row_number > 1
            prs.delete()
