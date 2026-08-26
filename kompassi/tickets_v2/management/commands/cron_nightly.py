import logging

from django.core.management.base import BaseCommand

from kompassi.core.utils.cleanup import perform_cleanup

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    # NOTE: this lives under tickets_v2 for historical reasons, but perform_cleanup() is
    # global (OAuth tokens, sessions, and whatever else registers @register_cleanup).
    # tickets_v2's own periodic work has moved to cron_frequent.
    help = "Run scheduled tasks"

    def handle(self, *args, **options):
        try:
            perform_cleanup()
        except RuntimeError as e:
            logger.error("Error occurred while performing cleanup", exc_info=e)
