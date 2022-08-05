from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand

from ...models import Privilege, SlackAccess


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

            slack_access, created = SlackAccess.objects.get_or_create(
                privilege=privilege,
                defaults=dict(
                    team_name=team_name,
                ),
            )
