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

        self.venue, unused = Venue.objects.get_or_create(name='Kongressitalo Mikaeli', defaults=dict(
            name_inessive='Kongressitalo Mikaelissa',
        ))
        self.event, unused = Event.objects.get_or_create(slug='mimicon2015', defaults=dict(
            name='Mimicon 2015',
            name_genitive='Mimicon 2015 -tapahtuman',
            name_illative='Mimicon 2015 -tapahtumaan',
            name_inessive='Mimicon 2015 -tapahtumassa',
            homepage_url='http://www.mimicon.fi',
            organization_name='MAMY Mikkelin Anime ja Manga Yhdistys ry',
            organization_url='http://mamy.animeunioni.org/',
            start_time=datetime(2015, 6, 13, 10, 0, tzinfo=self.tz),
            end_time=datetime(2015, 6, 14, 18, 0, tzinfo=self.tz),
            venue=self.venue,
        ))

    def setup_tickets(self):
        from tickets.models import TicketsEventMeta, LimitGroup, Product

        tickets_admin_group, = TicketsEventMeta.get_or_create_groups(self.event, ['admins'])

        defaults = dict(
            admin_group=tickets_admin_group,
            due_days=14,
            shipping_and_handling_cents=0,
            reference_number_template="2015{:05d}",
            contact_email='Mimicon <lipunmyynti@mimicon.fi>',
            ticket_free_text="Tämä on sähköinen lippusi Mimicon 2015 -tapahtumaan. Sähköinen lippu vaihdetaan rannekkeeseen\n"
                "lipunvaihtopisteessä saapuessasi tapahtumaan. Voit tulostaa tämän lipun tai näyttää sen\n"
                "älypuhelimen tai tablettitietokoneen näytöltä. Mikäli kumpikaan näistä ei ole mahdollista, ota ylös\n"
                "kunkin viivakoodin alla oleva neljästä tai viidestä sanasta koostuva sanakoodi ja ilmoita se\n"
                "lipunvaihtopisteessä.\n\n"
                "Tervetuloa Mimiconiin!",
            front_page_text="<h2>Tervetuloa ostamaan pääsylippuja Mimicon 2015 -tapahtumaan!</h2>"
                "<p>Liput maksetaan suomalaisilla verkkopankkitunnuksilla heti tilauksen yhteydessä.</p>"
                "<p>Lue lisää tapahtumasta <a href='http://www.mimicon.fi'>Mimiconin kotisivuilta</a>.</p>",
            print_logo_path = mkpath('static', 'images', 'Mimicon2015_logo.png'),
            print_logo_width_mm = 30,
            print_logo_height_mm = 30,
        )

        if self.test:
            t = now()
            defaults.update(
                ticket_sales_starts=t - timedelta(days=60),
                ticket_sales_ends=t + timedelta(days=60),
            )
        else:
            defaults.update(
                ticket_sales_starts=datetime(2015, 3, 2, 18, 0, tzinfo=self.tz),
                #ticket_sales_ends=datetime(2015, 1, 11, 18, 0, tzinfo=self.tz),
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
                name='Mimicon 2015 -pääsylippu',
                description='Lippu kattaa koko viikonlopun. Maksettuasi sinulle lähetetään PDF-lippu antamaasi sähköpostiin, jota vastaan saat rannekkeen tapahtuman ovelta.',
                limit_groups=[
                    limit_group('Pääsyliput', 500),
                ],
                price_cents=1500,
                requires_shipping=False,
                electronic_ticket=True,
                available=True,
                ordering=ordering(),
            ),
            dict(
                name='Lattiamajoituspaikka',
                description='Lattiamajoituspaikka lauantain ja sunnuntain väliseksi yöksi. Tarvitset oman makuupussin ja -alustan. Lattiamajoituksesta ei lähetetä erillistä lippua, vaan lattiamajoitus toimii nimi listaan -periaatteella.',
                limit_groups=[
                    limit_group('Lattiamajoitus', 80),
                ],
                price_cents=500,
                requires_shipping=False,
                electronic_ticket=False,
                available=True,
                ordering=ordering(),
            ),
            dict(
                name='Lounaslippu',
                description='Tällä lipukkeella saat herkullisen lounaan ravintola Napostellasta kumpana tahansa tapahtumapäivänä. Lounasliput toimitetaan samalla PDF-lipulla pääsylippujesi kanssa.',
                limit_groups=[
                    limit_group('Lounas', 100),
                ],
                price_cents=780,
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
    help = 'Setup mimicon2015 specific stuff'

    def handle(self, *args, **opts):
        Setup().setup(test=settings.DEBUG)
