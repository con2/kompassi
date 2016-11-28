# encoding: utf-8

from __future__ import unicode_literals

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

        self.venue, unused = Venue.objects.get_or_create(name='Scandic Marina Congress Center', defaults=dict(
            name_inessive='Scandic Marina Congress Centerissä',
        ))
        self.event, unused = Event.objects.get_or_create(slug='popcult2017', defaults=dict(
            name='Popcult Helsinki 2017',
            name_genitive='Popcult Helsinki 2017 -tapahtuman',
            name_illative='Popcult Helsinki 2017 -tapahtumaan',
            name_inessive='Popcult Helsinki 2017 -tapahtumassa',
            homepage_url='http://popcult.fi/helsinki-2017',
            organization_name='Finnish Fandom Conventions ry',
            organization_url='http://popcult.fi',
            start_time=datetime(2017, 5, 6, 10, 0, tzinfo=self.tz),
            end_time=datetime(2017, 5, 7, 18, 0, tzinfo=self.tz),
            venue=self.venue,
        ))

    def setup_tickets(self):
        from tickets.models import TicketsEventMeta, LimitGroup, Product

        tickets_admin_group, = TicketsEventMeta.get_or_create_groups(self.event, ['admins'])

        defaults = dict(
            admin_group=tickets_admin_group,
            due_days=14,
            shipping_and_handling_cents=0,
            reference_number_template="2017{:05d}",
            contact_email='Popcult Helsinki <liput@popcult.fi>',
            plain_contact_email='liput@popcult.fi',
            ticket_free_text=
                "Tämä on sähköinen lippusi Popcult Helsinki 2017 -tapahtumaan. Sähköinen lippu vaihdetaan\n"
                "rannekkeeseen lipunvaihtopisteessä saapuessasi tapahtumaan. Voit tulostaa tämän lipun tai\n"
                "näyttää sen älypuhelimen tai tablettitietokoneen näytöltä. Mikäli kumpikaan näistä ei ole\n"
                "mahdollista, ota ylös kunkin viivakoodin alla oleva neljästä tai viidestä sanasta koostuva\n"
                "Kissakoodi ja ilmoita se lipunvaihtopisteessä.\n\n"
                "Tervetuloa Popcult Helsinkiin!",
            front_page_text=u"<h2>Tervetuloa ostamaan pääsylippuja Popcult Helsinki 2017 -tapahtumaan!</h2>"
                "<p>Liput maksetaan suomalaisilla verkkopankkitunnuksilla heti tilauksen yhteydessä.</p>"
                "<p>Lue lisää tapahtumasta <a href='http://popcult.fi/helsinki-2017'>Popcult Helsinki 2017 -tapahtuman kotisivuilta</a>.</p>",
        )

        if self.test:
            t = now()
            defaults.update(
                ticket_sales_starts=t - timedelta(days=60),
                ticket_sales_ends=t + timedelta(days=60),
            )
        else:
            defaults.update(
                ticket_sales_starts=datetime(2016, 12, 5, 18, 0, tzinfo=self.tz),
                # ticket_sales_ends=datetime(2015, 1, 11, 18, 0, tzinfo=self.tz),
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
                name='Popcult Helsinki 2017 -pääsylippu',
                description='Lippu kattaa koko viikonlopun. Maksettuasi sinulle lähetetään PDF-lippu antamaasi sähköpostiin, jota vastaan saat rannekkeen tapahtuman ovelta.',
                limit_groups=[
                    limit_group('Pääsyliput', 2000),
                ],
                price_cents=2600,
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

        # v5
        if not meta.print_logo_path:
            meta.print_logo_path = mkpath('static', 'images', 'popcult.png')
            meta.print_logo_width_mm = 30
            meta.print_logo_height_mm = 30
            meta.save()

    def setup_payments(self):
        from payments.models import PaymentsEventMeta
        PaymentsEventMeta.get_or_create_dummy(event=self.event)


class Command(BaseCommand):
    args = ''
    help = 'Setup popcult2017 specific stuff'

    def handle(self, *args, **opts):
        Setup().setup(test=settings.DEBUG)
