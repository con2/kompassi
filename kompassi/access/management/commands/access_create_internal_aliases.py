from django.core.management.base import BaseCommand


class Command(BaseCommand):
    args = "[event_slug...]"
    help = "Create missing email aliases"

    def handle(*args, **opts):
        from kompassi.access.models import InternalEmailAlias

        InternalEmailAlias.ensure_internal_email_aliases()
