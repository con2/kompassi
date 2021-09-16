from django.core.management.base import BaseCommand
from django.utils.timezone import now


class Command(BaseCommand):
    help = "Prune expired CBAC entries"

    def handle(*args, **opts):
        from access.models import CBACEntry

        CBACEntry.prune_expired()
