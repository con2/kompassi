# encoding: utf-8

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand

from ...models import Privilege, SlackAccess


class Command(BaseCommand):
    def handle(*args, **opts):
        for slug, title, team_name in [
            ('tracon-slack', 'Traconin Slack-yhteisö', 'traconfi'),
            ('desuslack', 'Desuconin Slack-yhteisö', 'desucon'),
        ]:
            privilege, created = Privilege.objects.get_or_create(
                slug=slug,
                defaults=dict(
                    title=title,
                    description='''
<p>Slack on reaaliaikainen chat-palvelu, jota voi käyttää selaimella, mobiilisovelluksilla sekä
työpöytäsovelluksilla. Tämä tapahtuma käyttää Slackia järjestäjien, työvoiman ja ohjelmanjärjestäjien väliseen
kommunikointiin. Slackin käyttö on vapaaehtoista mutta erittäin suositeltavaa.</p>

<p>Slackiin tarvitset erillisen käyttäjätunnuksen, jonka saat pyytämällä kutsua alla olevalla
painikkeella. Kutsu lähetetään Kompassiin tallentamaasi sähköpostiosoitteeseen, ja sen saapumisessa voi
kestää joitain minuutteja.</p>

<p><strong>Slack on kolmannen osapuolen tuottama palvelu.</strong> Pyytämällä kutsua hyväksyt,
että sähköpostiosoitteesi luovutetaan Slackille kutsun lähettämistä ja käyttäjätunnuksen luomista varten. <a
href="https://slack.com/privacy-policy" target='_blank'>Lisätietoja Slackin yksityisyydensuojasta</a>.</p>

<p><strong>Slack näyttää sähköpostiosoitteesi muille tämän Slack-yhteisön jäsenille.</strong> Tätä ei valitettavasti
voi estää. Mikäli haluat pääsyn Slackiin muulla kuin Kompassiin tallentamallasi sähköpostiosoitteella, älä käytä tätä
toimintoa pääsyn pyytämiseen, vaan pyydä pääsyä sähköpostitse os. <em>{default_from_email}</em>. Mikäli
et halua näyttää mitään sähköpostiosoitetta muille tämän Slack-yhteisön jäsenille, et valitettavasti voi käyttää
Slackia.</p>
                    '''.strip().format(default_from_email=settings.DEFAULT_FROM_EMAIL),
                    request_success_message='Kutsu Slackiin on lähetetty sähköpostiisi.',
                    grant_code='access.privileges:invite_to_slack',
                )
            )

            slack_access, created = SlackAccess.objects.get_or_create(
                privilege=privilege,
                defaults=dict(
                    team_name=team_name,
                )
            )
