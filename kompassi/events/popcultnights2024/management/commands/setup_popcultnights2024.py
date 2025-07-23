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
            slug="popcultnights2024",
            defaults=dict(
                name="Popcult Nights: Halloween Edition (2024)",
                name_genitive="Popcult Nightsin",
                name_illative="Popcult Nightsiin",
                name_inessive="Popcult Nightsissä",
                homepage_url="https://popcult.fi/nights-2024-halloween-edition/",
                organization=self.organization,
                start_time=datetime(2024, 11, 2, 19, 0, tzinfo=self.tz),
                end_time=datetime(2024, 11, 2, 23, 0, tzinfo=self.tz),
                venue=self.venue,
            ),
        )

    def setup_tickets(self):
        from kompassi.zombies.tickets.models import LimitGroup, Product, TicketsEventMeta

        (tickets_admin_group,) = TicketsEventMeta.get_or_create_groups(self.event, ["admins"])

        t = now()
        defaults = dict(
            admin_group=tickets_admin_group,
            reference_number_template="2024{:05d}",
            contact_email="Popcult Helsinki <liput@popcult.fi>",
            ticket_free_text="Tämä on sähköinen lippusi Popcult Nights: Halloween Edition (2024) -tapahtumaan. Voit tulostaa tämän lipun tai\n"
            "näyttää sen älypuhelimen tai tablettitietokoneen näytöltä. Mikäli kumpikaan näistä ei ole\n"
            "mahdollista, ota ylös kunkin viivakoodin alla oleva neljästä tai viidestä sanasta koostuva\n"
            "Kissakoodi ja ilmoita se lipunvaihtopisteessä.\n\n"
            "Tervetuloa Popcult Nightsiin!",
            front_page_text="<h2>Tervetuloa ostamaan pääsylippuja Popcult Nights: Halloween Edition (2024) -tapahtumaan!</h2>"
            "<p>Liput maksetaan suomalaisilla verkkopankkitunnuksilla heti tilauksen yhteydessä.</p>"
            "<p>Lue lisää tapahtumasta <a href='https://popcult.fi/nights-2024-halloween-edition/'>Popcult Nights: Halloween Edition (2024) -tapahtuman kotisivuilta</a>.</p>",
            ticket_sales_starts=t,
            ticket_sales_ends=t + timedelta(days=60) if self.test else self.event.end_time,
        )

        TicketsEventMeta.objects.update_or_create(
            event=self.event,
            create_defaults=defaults,
            defaults=dict(),
        )

        def limit_group(description, limit):
            limit_group, _ = LimitGroup.objects.get_or_create(
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
                name="Popcult Nights: Halloween Edition (2024) -pääsylippu (K18)",
                description="Yksi pääsylippu Popcult Nights -tapahtumaan. Sisältää narikan.",
                limit_groups=[
                    limit_group("Pääsyliput", 400),
                ],
                price_cents=1700,
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
    help = "Setup popcultnights2024 specific stuff"

    def handle(self, *args, **opts):
        Setup().setup(test=settings.DEBUG)
