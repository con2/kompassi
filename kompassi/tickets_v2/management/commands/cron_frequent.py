import logging

from django.core.management.base import BaseCommand

from ...cron import tickets_v2_cron_frequent

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Run frequently scheduled tasks"

    def handle(self, *args, **options):
        try:
            tickets_v2_cron_frequent()
        except RuntimeError as e:
            logger.error("Error occurred while running frequent scheduled tasks for tickets_v2", exc_info=e)
