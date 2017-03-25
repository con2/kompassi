# encoding: utf-8



import os
from datetime import datetime, timedelta

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.timezone import now

from dateutil.tz import tzlocal

from core.utils import slugify


def mkpath(*parts):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', *parts))


class Setup(object):
    def setup(self, test=False):
        self.test = test
        self.tz = tzlocal()
        self.setup_core()
        self.setup_tickets()
        self.setup_payments()

    def setup_core(self):
        from core.models import Venue, Event

        self.venue, unused = Venue.objects.get_or_create(name='Messukeskuksen Kokoustamo', defaults=dict(
            name_inessive='Messukeskuksen Kokoustamossa',
        ))
        self.event, unused = Event.objects.get_or_create(slug='ropecon2017', defaults=dict(
            name='Ropecon (2017)',
            name_genitive='Ropeconin',
            name_illative='Ropeconiin',
            name_inessive='Ropeconissa',
            homepage_url='http://ropecon.fi',
            organization_name='Ropecon ry',
            organization_url='http://ropecon.fi/hallitus',
            start_time=datetime(2017, 7, 28, 15, 0, tzinfo=self.tz),
            end_time=datetime(2017, 7, 30, 18, 0, tzinfo=self.tz),
            venue=self.venue,
        ))

    def setup_tickets(self):
        from tickets.models import TicketsEventMeta, LimitGroup, Product, ShirtType, ShirtSize

        tickets_admin_group, = TicketsEventMeta.get_or_create_groups(self.event, ['admins'])

        defaults = dict(
            admin_group=tickets_admin_group,
            due_days=14,
            shipping_and_handling_cents=0,
            reference_number_template="2017{:05d}",
            contact_email='Ropeconin lipunmyynti <rahat@ropecon.fi>',
            front_page_text=(
                "<h2>Tervetuloa ostamaan pääsylippuja Ropeconiin!</h2>"
                "<p>Liput maksetaan suomalaisilla verkkopankkitunnuksilla heti tilauksen yhteydessä. Liput lähetetään "
                "sähköpostitse e-lippuina, jotka vaihdetaan rannekkeiksi saapuessasi tapahtumaan.</p>"
                "<p>Lue lisää tapahtumasta <a href='http://ropecon.fi'>Ropeconin kotisivuilta</a>.</p>"
            ),
        )

        if self.test:
            t = now()
            defaults.update(
                ticket_sales_starts=t - timedelta(days=60),
                ticket_sales_ends=t + timedelta(days=60),
            )
        else:
            # defaults.update(
            #     ticket_sales_starts=datetime(2015, 1, 25, 18, 0, tzinfo=self.tz),
            #     # ticket_sales_ends=datetime(2015, 1, 11, 18, 0, tzinfo=self.tz),
            # )
            pass

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
                name='Ropecon 2017 viikonloppulippu pe–su (Norppa & Kultisti -kampanja)',
                description=(
                    'Ropecon 2017 -tapahtuman pääsylippu, joka oikeuttaa kolmen päivän '
                    'sisäänpääsyrannekkeeseen. Kun tilaat lippusi 28.2. mennessä, saat myös Norppa & Kultisti '
                    '-kangasmerkin!'
                ),
                limit_groups=[
                    limit_group('Pääsyliput perjantai', 10000),
                    limit_group('Pääsyliput lauantai', 10000),
                    limit_group('Pääsyliput sunnuntai', 10000),
                ],
                price_cents=3500,
                requires_shipping=False,
                electronic_ticket=True,
                available=True,
                ordering=ordering(),
            ),
            dict(
                name='Ropecon 2017 viikonloppulippu pe–su',
                description=(
                    'Ropecon 2017 -tapahtuman pääsylippu, joka oikeuttaa kolmen päivän '
                    'sisäänpääsyrannekkeeseen.'
                ),
                limit_groups=[
                    limit_group('Pääsyliput perjantai', 10000),
                    limit_group('Pääsyliput lauantai', 10000),
                    limit_group('Pääsyliput sunnuntai', 10000),
                ],
                price_cents=3500,
                requires_shipping=False,
                electronic_ticket=True,
                available=False,
                ordering=ordering(),
            ),
            dict(
                name='Ropecon 2017 Conformers -paita',
                description=(
                    'T-paidat maksetaan ennakkoon ja noudetaan tapahtumasta. Paitakoot valitaan seuraavassa '
                    'vaiheessa. <a href="https://2017.ropecon.fi/spessupaita-2017/" target="_blank">Lue lisää '
                    'paitamalleista ja katso kokotaulukot</a>'
                ),
                limit_groups=[
                    limit_group('T-paidat', 10000),
                ],
                price_cents=3000,
                requires_shipping=False,
                electronic_ticket=True,
                requires_shirt_size=True,
                available=True,
                ordering=ordering(),
            ),

            # dict(
            #     name='Ropecon 2017 päivälippu perjantai',
            #     description='Ropecon 2017 tapahtuman pääsylippu oikeuttaen yhden päivän sisäänpääsyrannekkeeseen.',
            #     limit_groups=[
            #         limit_group('Pääsyliput perjantai', 10000),
            #     ],
            #     price_cents=2200,
            #     requires_shipping=False,
            #     electronic_ticket=True,
            #     available=True,
            #     ordering=ordering(),
            # ),
            # dict(
            #     name='Ropecon 2017 päivälippu lauantai',
            #     description='Ropecon 2017 tapahtuman pääsylippu oikeuttaen yhden päivän sisäänpääsyrannekkeeseen.',
            #     limit_groups=[
            #         limit_group('Pääsyliput lauantai', 10000),
            #     ],
            #     price_cents=2200,
            #     requires_shipping=False,
            #     electronic_ticket=True,
            #     available=True,
            #     ordering=ordering(),
            # ),
            # dict(
            #     name='Ropecon 2017 päivälippu sunnuntai',
            #     description='Ropecon 2017 tapahtuman pääsylippu oikeuttaen yhden päivän sisäänpääsyrannekkeeseen.',
            #     limit_groups=[
            #         limit_group('Pääsyliput sunnuntai', 10000),
            #     ],
            #     price_cents=1500,
            #     requires_shipping=False,
            #     electronic_ticket=True,
            #     available=True,
            #     ordering=ordering(),
            # ),
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

        for shirt_type_name, shirt_size_names in [
            ('Unisex-T-paita', ['XS', 'S', 'M', 'L', 'XL', 'XXL', '3XL', '4XL']),
            ('Naisten muotoonleikattu paita', ['XS', 'S', 'M', 'L', 'XL', 'XXL']),
            ('Miesten muotoonleikattu paita', ['S', 'M', 'L', 'XL', 'XXL']),
        ]:
            for shirt_color in [
                'Musta',
            ]:
                shirt_type, created = ShirtType.objects.get_or_create(
                    event=self.event,
                    name='{shirt_type_name} – {shirt_color}'.format(
                        shirt_type_name=shirt_type_name,
                        shirt_color=shirt_color,
                    ),
                )

                for shirt_size_name in shirt_size_names:
                    ShirtSize.objects.get_or_create(
                        type=shirt_type,
                        name=shirt_size_name,
                    )

    def setup_payments(self):
        from payments.models import PaymentsEventMeta
        PaymentsEventMeta.get_or_create_dummy(event=self.event)


class Command(BaseCommand):
    args = ''
    help = 'Setup ropecon2017 specific stuff'

    def handle(self, *args, **opts):
        Setup().setup(test=settings.DEBUG)
