# encoding: utf-8

from django.core.management import call_command
from django.core.management.base import BaseCommand, make_option

from ...models import Privilege


class Command(BaseCommand):
    def handle(*args, **opts):
        Privilege.objects.get_or_create(
            slug='tracon-slack',
            defaults=dict(
                title=u'Traconin Slack-yhteisö',
                description=u'''
<p>Slack on reaaliaikainen chat-palvelu, jota voi käyttää selaimella, mobiilisovelluksilla sekä
työpöytäsovelluksilla. Tracon käyttää Slackia conitean, työvoiman ja ohjelmanjärjestäjien väliseen
kommunikointiin. Slackin käyttö on vapaaehtoista mutta erittäin suositeltavaa.</p>

<p>Slackiin tarvitset erillisen käyttäjätunnuksen, jonka saat pyytämällä kutsua alla olevalla
painikkeella. Kutsu lähetetään Kompassiin tallentamaasi sähköpostiosoitteeseen, ja sen saapumisessa voi
kestää joitain minuutteja.</p>

<p><strong>Slack on kolmannen osapuolen tuottama palvelu.</strong> Pyytämällä kutsua hyväksyt,
että sähköpostiosoitteesi luovutetaan Slackille kutsun lähettämistä ja käyttäjätunnuksen luomista varten. <a
href="https://slack.com/privacy-policy" target='_blank'>Lisätietoja Slackin yksityisyydensuojasta</a>.</p>

<p><strong>Slack näyttää sähköpostiosoitteesi muille Traconin Slack-yhteisön jäsenille.</strong> Tätä ei valitettavasti
voi estää. Mikäli haluat pääsyn Slackiin muulla kuin Kompassiin tallentamallasi sähköpostiosoitteella, älä käytä tätä
toimintoa pääsyn pyytämiseen, vaan pyydä pääsyä Japsulta sähköpostitse os. <em>japsu@tracon.fi</em>. Mikäli
et halua näyttää mitään sähköpostiosoitetta muille Traconin Slack-yhteisön jäsenille, et valitettavasti voi käyttää
Traconin Slackia.</p>
                '''.strip(),
                request_success_message=u'Kutsu Traconin Slackiin on lähetetty sähköpostiisi.',
                grant_code='access.privileges:invite_to_slack',
            )
        )
