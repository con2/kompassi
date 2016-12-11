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

        self.venue = Venue.objects.get(name='Kulttuuriareena Gloria')
        self.event, unused = Event.objects.get_or_create(slug='lookingforalice', defaults=dict(
            name='Looking for Alice',
            name_genitive='Looking for Alice -tapahtuman',
            name_illative='Looking for Alice -tapahtumaan',
            name_inessive='Looking for Alice -tapahtumassa',
            homepage_url='http://www.hellocon.fi',
            organization_name='Hellocon ry',
            organization_url='http://www.hellocon.fi',
            start_time=datetime(2017, 2, 18, 10, 0, tzinfo=self.tz),
            end_time=datetime(2017, 2, 18, 18, 0, tzinfo=self.tz),
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
            contact_email='Looking for Alice <tickets.lookingforalice@gmail.com>',
            plain_contact_email='tickets.lookingforalice@gmail.com',
            ticket_free_text=(
                "Tämä on sähköinen lippusi Looking for Alice -tapahtumaan. Voit tulostaa tämän lipun tai\n"
                "näyttää sen älypuhelimen tai tablettitietokoneen näytöltä. Mikäli kumpikaan näistä ei ole\n"
                "mahdollista, ota ylös kunkin viivakoodin alla oleva neljästä tai viidestä sanasta koostuva\n"
                "Kissakoodi ja ilmoita se lipunvaihtopisteessä.\n\n"

                "This is your electronic ticket to Looking for Alice. You can print it or show it from your\n"
                "smartphone or tablet. If neither of these are suitable for you, please write down the four\n"
                "to six Finnish words under the barcode – they will function as your ticket code at the\n"
                "ticket exchange point.\n\n"

                "Tervetuloa Looking for Alice -tapahtumaan! Welcome to Looking for Alice!"
            ),
            front_page_text=(
                "<h2>Tervetuloa ostamaan pääsylippuja Looking for Alice -tapahtumaan!</h2>"
                "<p>Liput maksetaan suomalaisilla verkkopankkitunnuksilla tai luottokortilla heti tilauksen yhteydessä.</p>"

                "<h2>Welcome to the Looking for Alice ticket shop!</h2>"
                "<p>We accept Finnish Internet bank payments and international credit cards.</p>"
            ),
        )

        if self.test:
            t = now()
            defaults.update(
                ticket_sales_starts=t - timedelta(days=60),
                ticket_sales_ends=t + timedelta(days=60),
            )
        else:
            defaults.update(
                ticket_sales_starts=datetime(2016, 12, 11, 18, 0, tzinfo=self.tz),
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
                name='The White Rabbit',
                description=(
                    'The White Rabbit -lippu johdattaa sinut seikkailuun sekä In The Wonderland -päiväosioon että Through the Looking Glass -iltaosioon.\n\n'
                    'The White Rabbit – a regular full day ticket, includes entrance to the In the Wonderland day section and Through the Looking Glass evening section.'
                ),
                limit_groups=[
                    limit_group('The White Rabbit', 130),
                ],
                price_cents=5500,
                requires_shipping=False,
                electronic_ticket=True,
                available=True,
                ordering=ordering(),
            ),
            dict(
                name='The White Rabbit',
                description=(
                    'Kuninkaallisen menon takaa The Queen of Hearts-lippu, jolla pääset päiväosioon aikaisemmin sisälle ja saat sisäänpääsyn Through the Looking Glass -iltaosioon. Lisäksi lippu sisältää kuva-session upeiden kunniavieraidemme kanssa ihanan Sanni Siiran kuvaamana sekä pienen lahjakassin!\n\n'
                    'The Queen of Hearts – Vip full day ticket, includes early entrance to the In the Wonderland day section and entrance to the Through the looking Glass evening section. The ticket also includes a small goodie bag and a photosession with the guests of honors by Sanni Siira!'
                ),
                limit_groups=[
                    limit_group('The Queen of Hearts', 30),
                ],
                price_cents=7000,
                requires_shipping=False,
                electronic_ticket=True,
                available=True,
                ordering=ordering(),
            ),
            dict(
                name='Through the Looking Glass',
                description=(
                    'Through the Looking Glass -lipulla pääset osallistumaan Through the Looking Glass -iltaosioon.\n\n'
                    'Through the Looking Glass – evening section ticket. This ticket allows an entrance to the Through the Looking Glass evening section of the event.'
                ),
                limit_groups=[
                    limit_group('Through the Looking Glass', 100),
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
    help = 'Setup lookingforalice specific stuff'

    def handle(self, *args, **opts):
        Setup().setup(test=settings.DEBUG)
