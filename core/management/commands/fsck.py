import logging
from typing import Iterable

from django.core.management.base import BaseCommand

from labour.models.roster import Shift

from ...models import Event


logger = logging.getLogger("kompassi")


class Command(BaseCommand):
    args = ""
    help = "Check data integrity"

    events: Iterable[Event]

    def add_arguments(self, parser):
        parser.add_argument("--event", nargs="*", metavar="SLUG", help="Events to process (default all)")

    def handle(self, *args, **options):
        if options["events"]:
            self.events = Event.objects.filter(slug__in=options["events"])
        else:
            self.events = Event.objects.all()

        self.labour_check_shifts()

    def labour_check_shifts(self):
        for shift in Shift.objects.filter(signup__event__in=self.events):
            jc = shift.job.job_category
            signup = shift.signup
            if not signup.job_categories_accepted.filter(id=jc.id).exists():
                print(
                    f"{shift.signup.event.slug}: Job category of shift not present in "
                    f"accepted job categories of signup (shift = {shift.id}, jc = {jc.id}, signup = {signup.id})"
                )
