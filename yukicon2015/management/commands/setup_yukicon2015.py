# encoding: utf-8

from datetime import datetime, timedelta

from django.core.management.base import BaseCommand, make_option
from django.utils.timezone import get_default_timezone, now

from core.utils import slugify


class Setup(object):
    def setup(self, test=False):
        self.test = test
        self.tz = get_default_timezone()
        self.setup_core()
        self.setup_tickets()

    def setup_core(self):
        from core.models import Venue, Event

        self.venue, unused = Venue.objects.get_or_create(name='Espoon kulttuurikeskus', defaults=dict(
            name_inessive='Espoon kulttuurikeskuksessa',
        ))
        self.event, unused = Event.objects.get_or_create(slug='yukicon2015', defaults=dict(
            name='Yukicon 2.0',
            name_genitive='Yukicon 2.0 -tapahtuman',
            name_illative='Yukicon 2.0 -tapahtumaan',
            name_inessive='Yukicon 2.0 -tapahtumassa',
            homepage_url='http://www.yukicon.fi',
            organization_name='Yukitea ry',
            organization_url='http://www.yukicon.fi',
            start_time=datetime(2015, 1, 10, 10, 0, tzinfo=self.tz),
            end_time=datetime(2015, 1, 11, 18, 0, tzinfo=self.tz),
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
            contact_email='Yukicon <yukicon@yukicon.fi>',
            plain_contact_email='yukicon@yukicon.fi',
            ticket_free_text=u"Tämä on sähköinen lippusi Yukicon 2.0 -tapahtumaan. Sähköinen lippu vaihdetaan rannekkeeseen\n"
                u"lipunvaihtopisteessä saapuessasi tapahtumaan. Voit tulostaa tämän lipun tai näyttää sen\n"
                u"älypuhelimen tai tablettitietokoneen näytöltä. Mikäli kumpikaan näistä ei ole mahdollista, ota ylös\n"
                u"kunkin viivakoodin alla oleva neljästä tai viidestä sanasta koostuva sanakoodi ja ilmoita se\n"
                u"lipunvaihtopisteessä.\n\n"
                u"Tervetuloa Yukiconiin!",
            front_page_text=u"<h2>Tervetuloa ostamaan pääsylippuja Yukicon 2.0 -tapahtumaan!</h2>"
                u"<p>Liput maksetaan suomalaisilla verkkopankkitunnuksilla heti tilauksen yhteydessä.</p>"
                u"<p>Lue lisää tapahtumasta <a href='http://www.yukicon.fi'>Yukiconin kotisivuilta</a>.</p>",
        )

        if self.test:
            t = now()
            defaults.update(
                ticket_sales_starts=t - timedelta(days=60),
                ticket_sales_ends=t + timedelta(days=60),
            )
        else:
            defaults.update(
                ticket_sales_starts=datetime(2014, 11, 20, 18, 0, tzinfo=self.tz),
                ticket_sales_ends=datetime(2015, 1, 11, 18, 0, tzinfo=self.tz),
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
                name=u'Yukicon 2015 -pääsylippu',
                description=u'Lippu kattaa koko viikonlopun. Maksettuasi sinulle lähetetään PDF-lippu antamaasi sähköpostiin, jota vastaan saat rannekkeen tapahtuman ovelta.',
                limit_groups=[
                    limit_group('Lauantain liput', 1450),
                ],
                price_cents=1700,
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


class Command(BaseCommand):
    args = ''
    help = 'Setup yukicon2015 specific stuff'

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
