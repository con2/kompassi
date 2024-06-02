import logging

from django.core.management.base import BaseCommand

from ...models.intra_event_meta import IntraEventMeta

logger = logging.getLogger("kompassi")


class Command(BaseCommand):
    args = ""
    help = "Setup intra app"

    def handle(self, *args, **options):
        # tracon ry events since tracon 2016 have dynamic organizer listing in tracontent/wp
        IntraEventMeta.objects.filter(
            event__organization__slug="tracon-ry",
            event__start_time__gte="2016-01-01",
        ).update(
            is_organizer_list_public=True,
        )
