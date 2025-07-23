import os
from datetime import datetime, timedelta

from dateutil.tz import tzlocal
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.timezone import now


def mkpath(*parts):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", *parts))


class Setup:
    def __init__(self):
        self._ordering = 0

    def get_ordering_number(self):
        self._ordering += 10
        return self._ordering

    def setup(self, test=False):
        self.test = test
        self.tz = tzlocal()
        self.setup_core()
        # self.setup_tickets()

    def setup_core(self):
        from kompassi.core.models import Event, Organization, Venue

        self.venue, unused = Venue.objects.get_or_create(
            name="Tiivistämö",
            defaults=dict(
                name_inessive="Tiivistämöllä",
            ),
        )
        self.organization, unused = Organization.objects.get_or_create(
            slug="finnish-fandom-conventions-ry",
            defaults=dict(
                name="Finnish Fandom Conventions ry",
                homepage_url="http://popcult.fi",
            ),
        )
        self.event, unused = Event.objects.get_or_create(
            slug="popcultnights2023",
            defaults=dict(
                name="Popcult Nights 2023",
                name_genitive="Popcult Nights 2023 -tapahtuman",
                name_illative="Popcult Nights 2023 -tapahtumaan",
                name_inessive="Popcult Nights 2023 -tapahtumassa",
                homepage_url="http://popcult.fi/nights-2023",
                organization=self.organization,
                start_time=datetime(2023, 10, 21, 19, 0, tzinfo=self.tz),
                end_time=datetime(2023, 10, 21, 23, 0, tzinfo=self.tz),
                venue=self.venue,
            ),
        )

    def setup_tickets(self):
        from kompassi.zombies.tickets.models import LimitGroup, Product, TicketsEventMeta

        (tickets_admin_group,) = TicketsEventMeta.get_or_create_groups(self.event, ["admins"])

        defaults = dict(
            admin_group=tickets_admin_group,
            reference_number_template="2023{:05d}",
            contact_email="Popcult Helsinki <liput@popcult.fi>",
            ticket_free_text="Tämä on sähköinen lippusi Popcult Nights 2023 -tapahtumaan. Voit tulostaa tämän lipun tai\n"
            "näyttää sen älypuhelimen tai tablettitietokoneen näytöltä. Mikäli kumpikaan näistä ei ole\n"
            "mahdollista, ota ylös kunkin viivakoodin alla oleva neljästä tai viidestä sanasta koostuva\n"
            "Kissakoodi ja ilmoita se lipunvaihtopisteessä.\n\n"
            "Tervetuloa Popcult Nightsiin!",
            front_page_text="<h2>Tervetuloa ostamaan pääsylippuja Popcult Nights 2023 -tapahtumaan!</h2>"
            "<p>Liput maksetaan suomalaisilla verkkopankkitunnuksilla heti tilauksen yhteydessä.</p>"
            "<p>Lue lisää tapahtumasta <a href='http://popcult.fi/nights-2023'>Popcult Nights 2023 -tapahtuman kotisivuilta</a>.</p>",
        )

        if self.test:
            t = now()
            defaults.update(
                ticket_sales_starts=t - timedelta(days=60),
                ticket_sales_ends=t + timedelta(days=60),
            )

        meta, unused = TicketsEventMeta.objects.get_or_create(event=self.event, defaults=defaults)

        def limit_group(description, limit):
            limit_group, unused = LimitGroup.objects.get_or_create(
                event=self.event,
                description=description,
                defaults=dict(limit=limit),
            )

            return limit_group

        def ordering():
            ordering.counter += 10
            return ordering.counter

        ordering.counter = 0

        for product_info in [
            dict(
                name="Popcult Nights 2023 -pääsylippu (K18)",
                description="Yksi pääsylippu Popcult Nights -tapahtumaan lauantaille 21.10. Sisältää narikan.",
                limit_groups=[
                    limit_group("Pääsyliput", 400),
                ],
                price_cents=1500,
                electronic_ticket=True,
                available=True,
                ordering=ordering(),
            ),
        ]:
            name = product_info.pop("name")
            limit_groups = product_info.pop("limit_groups")

            product, unused = Product.objects.get_or_create(event=self.event, name=name, defaults=product_info)

            if not product.limit_groups.exists():
                product.limit_groups.set(limit_groups)
                product.save()


class Command(BaseCommand):
    args = ""
    help = "Setup popcultnights2023 specific stuff"

    def handle(self, *args, **opts):
        Setup().setup(test=settings.DEBUG)
