from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create missing CBAC entries"

    def handle(*args, **opts):
        from kompassi.access.models import CBACEntry

        CBACEntry.ensure_admin_group_privileges()
