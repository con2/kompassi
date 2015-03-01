# encoding: utf-8

import os
from datetime import datetime, timedelta

from django.core.management.base import BaseCommand, make_option
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

        self.venue, unused = Venue.objects.get_or_create(name='Kuopion musiikkikeskus', defaults=dict(
            name_inessive='Kuopion musiikkikeskuksessa',
        ))
        self.event, unused = Event.objects.get_or_create(slug='animecon2015', defaults=dict(
            name='Animecon 2015',
            name_genitive='Animecon 2015 -tapahtuman',
            name_illative='Animecon 2015 -tapahtumaan',
            name_inessive='Animecon 2015 -tapahtumassa',
            homepage_url='http://2015.animecon.fi',
            organization_name='Nekocon ry',
            organization_url='http://animecon.fi',
            start_time=datetime(2015, 7, 11, 9, 30, tzinfo=self.tz),
            end_time=datetime(2015, 7, 12, 17, 0, tzinfo=self.tz),
            venue=self.venue,
        ))

    def setup_tickets(self):
        from tickets.models import TicketsEventMeta, LimitGroup, Product

        tickets_admin_group, unused = TicketsEventMeta.get_or_create_group(self.event, 'admins')

        defaults = dict(
            admin_group=tickets_admin_group,
            due_days=14,
            shipping_and_handling_cents=0,
            reference_number_template="2015{:05d}",
            contact_email='Animecon 2015 <liput@animecon.fi>',
            plain_contact_email='liput@animecon.fi',
            ticket_free_text=u"Tämä on sähköinen lippusi Animecon 2015 -tapahtumaan. Sähköinen lippu vaihdetaan rannekkeeseen\n"
                u"lipunvaihtopisteessä saapuessasi tapahtumaan. Voit tulostaa tämän lipun tai näyttää sen\n"
                u"älypuhelimen tai tablettitietokoneen näytöltä. Mikäli kumpikaan näistä ei ole mahdollista, ota ylös\n"
                u"kunkin viivakoodin alla oleva neljästä tai viidestä sanasta koostuva Kissakoodi ja ilmoita se\n"
                u"lipunvaihtopisteessä.\n\n"
                u"Tervetuloa Animecon 2015 -tapahtumaan!",
            front_page_text=u"<h2>Tervetuloa ostamaan pääsylippuja Animecon 2015 -tapahtumaan!</h2>"
                u"<p>Liput maksetaan suomalaisilla verkkopankkitunnuksilla heti tilauksen yhteydessä.</p>"
                u"<p>Lue lisää tapahtumasta <a href='http://2015.animecon.fi'>Animecon 2015 -tapahtuman kotisivuilta</a>.</p>"
                u"<p>Huom! Tämä verkkokauppa palvelee ainoastaan asiakkaita, joilla on osoite Suomessa. Mikäli tarvitset "
                u"toimituksen ulkomaille, ole hyvä ja ota sähköpostitse yhteyttä: <address>liput@animecon.fi</address>"
        )

        if self.test:
            t = now()
            defaults.update(
                ticket_sales_starts=t - timedelta(days=60),
                ticket_sales_ends=t + timedelta(days=60),
            )
        else:
            pass
            # defaults.update(
            #     ticket_sales_starts=datetime(2015, 1, 25, 18, 0, tzinfo=self.tz),
            #     # ticket_sales_ends=datetime(2015, 1, 11, 18, 0, tzinfo=self.tz),
            # )

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
                name=u'Animecon 2015 -pääsylippu',
                description=u'Viikonloppuranneke Kuopiossa järjestettävään Animecon-tapahtumaan. Huom. myynnissä vain viikonloppurannekkeita. Lippu lähetetään postitse.',
                limit_groups=[
                    limit_group('Pääsyliput', 3000),
                ],
                price_cents=1600,
                requires_shipping=True,
                electronic_ticket=False,
                available=True,
                ordering=ordering(),
            ),
            dict(
                name=u'Lattiamajoituspaikka (koko vkl)',
                description=u'Lattiamajoituspaikka molemmiksi öiksi pe-la ja la-su. Majoituksesta lisää tietoa sivuillamme www.animecon.fi.',
                limit_groups=[
                    limit_group('Lattiamajoitus pe-la', 445),
                    limit_group('Lattiamajoitus la-su', 445),
                ],
                price_cents=1000,
                requires_shipping=False,
                electronic_ticket=False,
                available=True,
                ordering=ordering(),
            ),
            dict(
                name=u'Lattiamajoituspaikka (pe-la)',
                description=u'Lattiamajoituspaikka perjantain ja lauantain väliseksi yöksi. Majoituksesta lisää tietoa sivuillamme www.animecon.fi.',
                limit_groups=[
                    limit_group('Lattiamajoitus pe-la', 445),
                ],
                price_cents=700,
                requires_shipping=False,
                electronic_ticket=False,
                available=True,
                ordering=ordering(),
            ),
            dict(
                name=u'Lattiamajoituspaikka (la-su)',
                description=u'Lattiamajoituspaikka lauantain ja sunnuntain väliseksi yöksi. Majoituksesta lisää tietoa sivuillamme www.animecon.fi.',
                limit_groups=[
                    limit_group('Lattiamajoitus la-su', 445),
                ],
                price_cents=700,
                requires_shipping=False,
                electronic_ticket=False,
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
            meta.print_logo_path = mkpath('static', 'images', 'animecon.png')
            meta.print_logo_width_mm = 30
            meta.print_logo_height_mm = 30
            meta.save()

    def setup_payments(self):
        from payments.models import PaymentsEventMeta
        PaymentsEventMeta.get_or_create_dummy(event=self.event)


class Command(BaseCommand):
    args = ''
    help = 'Setup animecon2015 specific stuff'

    option_list = BaseCommand.option_list + (
        make_option('--test',
            action='store_true',
            dest='test',
            default=False,
            help='Set the event up for testing',
        ),
    )

    def handle(self, *args, **opts):
        Setup().setup(test=opts['test'])
