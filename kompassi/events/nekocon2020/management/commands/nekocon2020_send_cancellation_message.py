import logging

from django.core.mail import EmailMessage
from django.core.management.base import BaseCommand

from kompassi.zombies.tickets.models import Order

logger = logging.getLogger(__name__)

FROM = "nekocon2020-tickets@kompassi.eu"
SUBJECT = "Nekocon 2020: Tapahtuma on peruttu"
MESSAGE = """NEKOCON ON PERUTTU!

Nekoconin conitea on aktiivisesti seurannut tilanteen kehittymistä ja
keskustellut tapahtuman tulevaisuudesta. Keskiviikkona 22.4. tulleessa
hallituksen tiedotustilaisuudessa yli 500 hengen yleisötapahtumat perutaan
heinäkuun loppuun saakka. Nekocon noudattaa hallituksen linjauksia
koronaepidemiassa ja peruu tapahtumansa 11.-12.7.2020 Kuopion
Musiikkikeskuksella.

Kiitämme kaikkia, jotka olisivat olleet osa tapahtumaamme, sillä ilman
teitä conia ei olisi voitu alkaa rakentamaan juuri teitä varten! Alla
ohjeita sinulle, joka olit tulossa osaksi tapahtumaamme, olitpa sitten
kävijä, ohjelmapitäjä tai muu taho.

Tapahtumaan lipun ostaneille palautetaan lippukuluista 24 € ja majoituksen
ostaneille 14 €. Lippua ja majoitusta kohden pidätetään 1€
maksuliikennekuluja. Palautukset hoidetaan pikimmiten pankkitilille, josta
tapahtuma lippu ja/tai majoitus on maksettu.

Nekoconiin hakeneille ohjelmapitäjille, vapaaehtoisille, sidosryhmille ja
sponsoreille lähetetään viestiä pikimmiten tapahtuman peruuntumista
koskien. Jos olet ilmoittautunut osaksi tapahtumaan, seuraathan siis
sähköpostiasi.

Olemme kaikki varmasti pahoillamme, ettei tapahtumaa päässyt tänä
kesänä syntymään, mutta conitea istuu alas pohtimaan tapahtuman
tulevaisuutta ja suuntaa katseensa ensi kesään. Nekoconin conitea toivottaa
kaikille vaikeista ajoista huolimatta aurinkoista kesää! Nekoconin Discord
myös jatkaa pyörimistä, jossa saa viettää kissojen tapaan letkeää
vapaa-aikaa!

Terveisin
Nekoconin conitea
"""


class Command(BaseCommand):
    args = ""
    help = "Send nekocon2020 cancellation message"

    def handle(self, *args, **opts):
        for order in Order.objects.filter(
            event__slug="nekocon2020",
            confirm_time__isnull=False,
            payment_date__isnull=False,
            cancellation_time__isnull=True,
        ):
            print(order.formatted_order_number, order.customer.name_and_email)

            EmailMessage(
                subject=SUBJECT,
                body=MESSAGE,
                from_email=FROM,
                to=(order.customer.name_and_email,),
            ).send(fail_silently=True)
