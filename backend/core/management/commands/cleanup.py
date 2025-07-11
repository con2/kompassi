from django.core.management.base import BaseCommand

from core.utils.cleanup import perform_cleanup


class Command(BaseCommand):
    help = "Run periodic cleanup on registered models."

    def handle(self, *args, **options):
        perform_cleanup()
