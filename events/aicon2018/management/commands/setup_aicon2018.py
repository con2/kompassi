from datetime import datetime, timedelta

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.timezone import now

from dateutil.tz import tzlocal

from core.utils import full_hours_between


class Setup(object):
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
        self.setup_payments()

    def setup_core(self):
        from core.models import Venue, Event

        self.venue, unused = Venue.objects.get_or_create(name='Kulttuuritalo (Helsinki)', defaults=dict(
            name_inessive='Kulttuuritalossa Helsingissä',
        ))
        self.event, unused = Event.objects.get_or_create(slug='aicon2018', defaults=dict(
            name='Aicon (2018)',
            name_genitive='Aiconin',
            name_illative='Aiconiin',
            name_inessive='Aiconissa',
            homepage_url='http://2018.aicon.fi',
            organization_name='Aicon ry',
            organization_url='http://aicon.fi',
            start_time=datetime(2018, 7, 7, 10, 0, tzinfo=self.tz),
            end_time=datetime(2018, 7, 7, 18, 0, tzinfo=self.tz),
            venue=self.venue,
        ))

    def setup_tickets(self):
        from tickets.models import TicketsEventMeta, LimitGroup, Product

        tickets_admin_group, = TicketsEventMeta.get_or_create_groups(self.event, ['admins'])

        defaults = dict(
            admin_group=tickets_admin_group,
            due_days=14,
            shipping_and_handling_cents=0,
            reference_number_template="2018{:05d}",
            contact_email='Aicon <liput@aicon.fi>',
            ticket_free_text=(
                "Tämä on sähköinen lippusi. Sähköinen lippu vaihdetaan rannekkeeseen\n"
                "lipunvaihtopisteessä saapuessasi tapahtumaan. Voit tulostaa tämän lipun tai näyttää sen\n"
                "älypuhelimen tai tablettitietokoneen näytöltä. Mikäli kumpikaan näistä ei ole mahdollista, ota ylös\n"
                "kunkin viivakoodin alla oleva neljästä tai viidestä sanasta koostuva sanakoodi ja ilmoita se\n"
                "lipunvaihtopisteessä.\n\n"
                "Tervetuloa tapahtumaan!"
            ),
            front_page_text=(
                "<h2>Tervetuloa ostamaan pääsylippuja vuoden 2018 Aiconiin!</h2>"
                "<p>Liput maksetaan suomalaisilla verkkopankkitunnuksilla heti tilauksen yhteydessä.</p>"
                "<p>Lue lisää tapahtumasta "
                "<a href='http://2018.aicon.fi' target='_blank'>Aiconin kotisivuilta</a>.</p>"
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
                name='VIP-lippu',
                description='Koko viikonlopun lippu Aiconiin huikein VIP-eduin!',
                limit_groups=[
                    limit_group('VIP-liput', 50),
                ],
                price_cents=3000,
                requires_shipping=False,
                electronic_ticket=True,
                available=True,
                ordering=self.get_ordering_number(),
            ),
            dict(
                name='Pääsylippu',
                description='Koko viikonlopun lippu Aiconiin.',
                limit_groups=[
                    limit_group('Viikonloppuliput', 800),
                ],
                price_cents=1500,
                requires_shipping=False,
                electronic_ticket=True,
                available=False,
                ordering=self.get_ordering_number(),
            ),
        ]:
            name = product_info.pop('name')
            limit_groups = product_info.pop('limit_groups')

            product, unused = Product.objects.get_or_create(
                event=self.event,
                name=name,
                defaults=product_info
            )

            if not product.limit_groups.exists():
                product.limit_groups = limit_groups
                product.save()

    def setup_payments(self):
        from payments.models import PaymentsEventMeta
        PaymentsEventMeta.get_or_create_dummy(event=self.event)


class Command(BaseCommand):
    args = ''
    help = 'Setup aicon2018 specific stuff'

    def handle(self, *args, **opts):
        Setup().setup(test=settings.DEBUG)
