import logging

from django.core.management.base import BaseCommand

from core.models.event import Event
from core.utils.log_utils import log_get_or_create

from ...models.response import Response

logger = logging.getLogger("kompassi")


class Command(BaseCommand):
    args = "[event_slug...]"
    help = "Create missing badges for Survey to Badge (STB) mappings"

    def add_arguments(self, parser):
        parser.add_argument(
            "event_slugs",
            nargs="+",
            metavar="EVENT_SLUG",
        )

    def handle(*args, **opts):
        for event_slug in opts["event_slugs"]:
            event = Event.objects.get(slug=event_slug)
            print(event.slug)

            for response in Response.objects.filter(
                form__event=event,
                superseded_by=None,
            ):
                badge, created = response.survey.workflow.ensure_survey_to_badge(response)
                if badge:
                    log_get_or_create(logger, badge, created)
                    logger.info(badge.perks)

            print()
