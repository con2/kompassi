import logging

from django.core.management.base import BaseCommand

from core.utils.cleanup import perform_cleanup

from ...cron import tickets_v2_cron_nightly

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Run scheduled tasks"

    def handle(self, *args, **options):
        try:
            tickets_v2_cron_nightly()
        except RuntimeError as e:
            logger.error("Error occurred while running scheduled tasks for tickets_v2", exc_info=e)

        try:
            perform_cleanup()
        except RuntimeError as e:
            logger.error("Error occurred while performing cleanup", exc_info=e)
