from django.core.management.base import BaseCommand


class Command(BaseCommand):
    args = "[event_slug...]"
    help = "Create missing badges for programme"

    def add_arguments(self, parser):
        parser.add_argument(
            "event_slugs",
            nargs="+",
            metavar="EVENT_SLUG",
        )

    def handle(*args, **opts):
        from core.models import Event
        from programme.models import Programme

        for event_slug in opts["event_slugs"]:
            event = Event.objects.get(slug=event_slug)

            if (meta := event.program_v2_event_meta) and meta.importer_name:
                raise ValueError(
                    "Due to the way this command is implemented, it is DANGEROUS to run "
                    "for events that have the V1 -> V2 import enabled. Doing so would "
                    "cause a storm of imports that would likely end up in several database deadlocks. "
                    "If you really need to do this, please disable the importer from ProgramV2Meta first, "
                    "run the command, reenable the importer and run program_v2_import_v1."
                )

            for programme in Programme.objects.filter(category__event=event):
                programme.apply_state()
