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
        self.event, unused = Event.objects.get_or_create(slug='ropecon2016', defaults=dict(
            name='Ropecon (2016)',
            name_genitive='Ropeconin',
            name_illative='Ropeconiin',
            name_inessive='Ropeconissa',
            homepage_url='http://ropecon.fi',
            organization_name='Ropecon ry',
            organization_url='http://ropecon.fi/hallitus',
            start_time=datetime(2016, 7, 29, 15, 0, tzinfo=self.tz),
            end_time=datetime(2016, 7, 31, 18, 0, tzinfo=self.tz),
            venue=self.venue,
        ))

    def setup_tickets(self):
        from tickets.models import TicketsEventMeta, LimitGroup, Product

        tickets_admin_group, = TicketsEventMeta.get_or_create_groups(self.event, ['admins'])

        defaults = dict(
            admin_group=tickets_admin_group,
            due_days=14,
            shipping_and_handling_cents=0,
            reference_number_template="2016{:05d}",
            contact_email='Ropeconin lipunmyynti <rahat@ropecon.fi>',
            plain_contact_email='rahat@ropecon.fi',
            front_page_text=u"<h2>Tervetuloa ostamaan pääsylippuja Ropeconiin!</h2>"
                u"<p>Liput maksetaan suomalaisilla verkkopankkitunnuksilla heti tilauksen yhteydessä. Liput lähetetään sähköpostitse e-lippuina, jotka vaihdetaan rannekkeiksi saapuessasi tapahtumaan.</p>"
                u"<p>Lue lisää tapahtumasta <a href='http://ropecon.fi'>Ropeconin kotisivuilta</a>.</p>",
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
                name=u'Ropecon 2016 viikonloppulippu pe-su',
                description=u'Ropecon 2016 tapahtuman pääsylippu oikeuttaen kolmen päivän sisäänpääsyrannekkeeseen.',
                limit_groups=[
                    limit_group('Pääsyliput perjantai', 10000),
                    limit_group('Pääsyliput lauantai', 10000),
                    limit_group('Pääsyliput sunnuntai', 10000),
                ],
                price_cents=3200,
                requires_shipping=False,
                electronic_ticket=True,
                available=True,
                ordering=ordering(),
            ),
            dict(
                name=u'Ropecon 2016 päivälippu perjantai',
                description=u'Ropecon 2016 tapahtuman pääsylippu oikeuttaen yhden päivän sisäänpääsyrannekkeeseen.',
                limit_groups=[
                    limit_group('Pääsyliput perjantai', 10000),
                ],
                price_cents=2200,
                requires_shipping=False,
                electronic_ticket=True,
                available=True,
                ordering=ordering(),
            ),
            dict(
                name=u'Ropecon 2016 päivälippu lauantai',
                description=u'Ropecon 2016 tapahtuman pääsylippu oikeuttaen yhden päivän sisäänpääsyrannekkeeseen.',
                limit_groups=[
                    limit_group('Pääsyliput lauantai', 10000),
                ],
                price_cents=2200,
                requires_shipping=False,
                electronic_ticket=True,
                available=True,
                ordering=ordering(),
            ),
          dict(
                name=u'Ropecon 2016 päivälippu sunnuntai',
                description=u'Ropecon 2016 tapahtuman pääsylippu oikeuttaen yhden päivän sisäänpääsyrannekkeeseen.',
                limit_groups=[
                    limit_group('Pääsyliput sunnuntai', 10000),
                ],
                price_cents=1500,
                requires_shipping=False,
                electronic_ticket=True,
                available=True,
                ordering=ordering(),
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
    help = 'Setup ropecon2016 specific stuff'

    def handle(self, *args, **opts):
        Setup().setup(test=settings.DEBUG)
