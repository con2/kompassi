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

        self.venue, unused = Venue.objects.get_or_create(name='Seinäjoen yhteiskoulu', defaults=dict(
            name_inessive='Seinäjoen yhteiskoululla',
        ))
        self.event, unused = Event.objects.get_or_create(slug='lakeuscon2016', defaults=dict(
            name='Lakeuscon',
            name_genitive='Lakeusconin',
            name_illative='Lakeusconiin',
            name_inessive='Lakeusconissa',
            homepage_url='http://www.lakeusconny.fi/',
            organization_name='Lakeuscon NY',
            organization_url='http://www.lakeusconny.fi/',
            start_time=datetime(2016, 5, 7, 10, 0, tzinfo=self.tz),
            end_time=datetime(2016, 5, 7, 20, 0, tzinfo=self.tz),
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
            contact_email='Lakeuscon NY <lakeusconny@lakeuscon.fi>',
            plain_contact_email='lakeusconny@lakeuscon.fi',
            ticket_free_text=u"Tämä on sähköinen lippusi Lakeusconiin. Sähköinen lippu vaihdetaan rannekkeeseen\n"
                u"lipunvaihtopisteessä saapuessasi tapahtumaan. Voit tulostaa tämän lipun tai näyttää sen\n"
                u"älypuhelimen tai tablettitietokoneen näytöltä. Mikäli kumpikaan näistä ei ole mahdollista, ota ylös\n"
                u"kunkin viivakoodin alla oleva neljästä tai viidestä sanasta koostuva Kissakoodi ja ilmoita se\n"
                u"lipunvaihtopisteessä.\n\n"
                u"Tervetuloa Lakeusconhin lauantaina 23. elokuuta 2016 Malmitalolle!",
            front_page_text=u"<h2>Tervetuloa ostamaan pääsylippuja Lakeusconiin!</h2>"
                u"<p>Liput maksetaan suomalaisilla verkkopankkitunnuksilla heti tilauksen yhteydessä.</p>"
                u"<p>Lue lisää tapahtumasta <a href='http://www.lakeusconny.fi'>Lakeusconin kotisivuilta</a>.</p>",
        )

        if self.test:
            t = now()
            defaults.update(
                ticket_sales_starts=t - timedelta(days=60),
                ticket_sales_ends=t + timedelta(days=60),
            )
        else:
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
                name=u'Lakeuscon-pääsylippu',
                description=u'Maksettuasi sinulle lähetetään PDF-lippu antamaasi sähköpostiin, jota vastaan saat rannekkeen tapahtuman ovelta.',
                limit_groups=[
                    limit_group('Pääsyliput', 500),
                ],
                price_cents=700,
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
    help = 'Setup lakeuscon2016 specific stuff'

    def handle(self, *args, **opts):
        Setup().setup(test=settings.DEBUG)
