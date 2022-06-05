from django.core.management.base import BaseCommand


class Command(BaseCommand):
    args = "[event_slug...]"
    help = "Archive signups for events"

    def add_arguments(self, parser):
        parser.add_argument(
            "event_slugs",
            nargs="+",
            metavar="EVENT_SLUG",
        )

    def handle(self, *args, **options):
        from labour.models import ArchivedSignup, Signup, EmptySignupExtra, LabourEventMeta
        from django.contrib.contenttypes.models import ContentType

        for signup in Signup.objects.filter(event__slug__in=options["event_slugs"]):
            ArchivedSignup.archive_signup(signup)

        empty_ctype = ContentType.objects.get_for_model(EmptySignupExtra)
        LabourEventMeta.objects.filter(event__slug__in=options["event_slugs"]).update(
            signup_extra_content_type=empty_ctype
        )
