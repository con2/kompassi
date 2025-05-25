import logging
from datetime import timedelta

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.timezone import now

from core.models import Person
from core.utils import log_get_or_create

from ...models import CBACEntry, Privilege, SlackAccess

logger = logging.getLogger("kompassi")


class Command(BaseCommand):
    def handle(*args, **opts):
        for slug, title, team_name in [
            ("tracon-slack", "Traconin Slack-yhteisö", "traconfi"),
            ("desuslack", "Desuconin Slack-yhteisö", "desucon"),
        ]:
            privilege, created = Privilege.objects.get_or_create(
                slug=slug,
                defaults=dict(
                    title=title,
                    description="""TODO WRITE ME""".strip().format(default_from_email=settings.DEFAULT_FROM_EMAIL),
                    request_success_message="",
                    grant_code="access.privileges:invite_to_slack",
                    url=f"https://{team_name}.slack.com",
                ),
            )

            log_get_or_create(logger, privilege, created)

            slack_access, created = SlackAccess.objects.get_or_create(
                privilege=privilege,
                defaults=dict(
                    team_name=team_name,
                ),
            )

            log_get_or_create(logger, slack_access, created)

        if settings.DEBUG:
            Person.get_or_create_dummy()

            # NOTE: claims={} effectively means "all privileges"
            entry, created = CBACEntry.objects.get_or_create(
                # ask Japsu why this is 1 and not a reference to the dummy user
                user_id=1,
                claims={},
                defaults=dict(
                    valid_from=now(),
                    valid_until=now() + timedelta(days=100 * 365),
                ),
            )

            log_get_or_create(logger, entry, created)
