from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Prune expired CBAC entries"

    def handle(*args, **opts):
        from access.models import CBACEntry

        CBACEntry.prune_expired()
