from datetime import datetime, timedelta

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.timezone import now
from django.urls import reverse

from dateutil.tz import tzlocal


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
        self.setup_tickets()

    def setup_core(self):
        from core.models import Organization, Venue, Event

        self.organization, unused = Organization.objects.get_or_create(
            slug="tracon-ry",
            defaults=dict(
                name="Tracon ry",
                homepage_url="https://ry.tracon.fi",
            ),
        )
        self.venue, unused = Venue.objects.get_or_create(name="Tampere-talo")
        self.event, unused = Event.objects.get_or_create(
            slug="tracon2023paidat",
            defaults=dict(
                name="Traconin hupparitilaus (2023)",
                name_genitive="Traconin hupparitilauksen",
                name_illative="Traconin hupparitilaukseen",
                name_inessive="Traconin hupparitilauksessa",
                homepage_url="http://2023.tracon.fi",
                organization=self.organization,
                start_time=datetime(2023, 9, 8, 16, 0, tzinfo=self.tz),
                end_time=datetime(2023, 9, 10, 18, 0, tzinfo=self.tz),
                venue=self.venue,
                public=False,
            ),
        )

    def setup_tickets(self):
        from tickets.models import TicketsEventMeta, LimitGroup, Product

        tickets_admin_group, pos_access_group = TicketsEventMeta.get_or_create_groups(self.event, ["admins", "pos"])

        defaults = dict(
            admin_group=tickets_admin_group,
            pos_access_group=pos_access_group,
            due_days=14,
            shipping_and_handling_cents=0,
            reference_number_template="2023{:06d}",
            contact_email="Traconin lipunmyynti <liput@tracon.fi>",
            front_page_text=(
                "<h2>Tervetuloa tilaamaan Traconin edustustuotteita!</h2>"
                "<p>HUOM! Tilaathan edustustuotteita tätä kautta vain, jos olet Traconin coniitti ja saanut ohjeistuksen siihen.</p>"
                "<p>Tuotteet maksetaan suomalaisilla verkkopankkitunnuksilla tai luottokortilla heti tilauksen yhteydessä.</p>"
                "<p><strong>Muista ilmoittaa tilattavien tuotteiden värit, koot, mallit ja nimikoinnit coniteawikin kautta!</strong></p>"
            ),
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

        for product_info in [
            dict(
                name="Vetoketjuhuppari",
                description="<p><strong>Muista ilmoittaa tilattavien tuotteiden värit, koot, mallit ja nimikoinnit coniteawikin kautta!</strong></p>",
                limit_groups=[
                    limit_group("Edustustuotteet", 9999),
                ],
                price_cents=1500,
                requires_shipping=False,
                electronic_ticket=False,
                available=True,
                ordering=self.get_ordering_number(),
            ),
            dict(
                name="Taskuhuppari",
                description="<p><strong>Muista ilmoittaa tilattavien tuotteiden värit, koot, mallit ja nimikoinnit coniteawikin kautta!</strong></p>",
                limit_groups=[
                    limit_group("Edustustuotteet", 9999),
                ],
                price_cents=1500,
                requires_shipping=False,
                electronic_ticket=False,
                available=True,
                ordering=self.get_ordering_number(),
            ),
            dict(
                name="Kauluspaita",
                description="<p><strong>Muista ilmoittaa tilattavien tuotteiden värit, koot, mallit ja nimikoinnit coniteawikin kautta!</strong></p>",
                limit_groups=[
                    limit_group("Edustustuotteet", 9999),
                ],
                price_cents=2000,
                requires_shipping=False,
                electronic_ticket=False,
                available=True,
                ordering=self.get_ordering_number(),
            ),
        ]:
            name = product_info.pop("name")
            limit_groups = product_info.pop("limit_groups")

            product, unused = Product.objects.get_or_create(event=self.event, name=name, defaults=product_info)

            if not product.limit_groups.exists():
                product.limit_groups.set(limit_groups)
                product.save()

        if not meta.receipt_footer:
            meta.receipt_footer = "Tracon ry / Y-tunnus 2886274-5 / liput@tracon.fi"
            meta.save()

class Command(BaseCommand):
    args = ""
    help = "Setup tracon2023 specific stuff"

    def handle(self, *args, **opts):
        Setup().setup(test=settings.DEBUG)
