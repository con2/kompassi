from django.core.management.base import BaseCommand
from django.utils.timezone import now


class Command(BaseCommand):
    help = "Create missing CBAC entries"

    def handle(*args, **opts):
        from access.models import CBACEntry

        CBACEntry.ensure_admin_group_privileges()
