from datetime import datetime, timedelta

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.timezone import now

from dateutil.tz import tzlocal


class Command(BaseCommand):
    def handle(self, *args, **opts):
        from core.models import Event, Organization, Venue
        from enrollment.models import EnrollmentEventMeta
        from payments.models import PaymentsEventMeta
        from tickets.models import TicketsEventMeta, LimitGroup, Product, ShirtType, ShirtSize

        tz = tzlocal()
        organization = Organization.objects.get(slug='tracon-ry')
        venue, unused = Venue.objects.get_or_create(name='Ilmoitetaan myöhemmin')
        event, unused = Event.objects.get_or_create(
            slug='traconpaidat2019',
            defaults=dict(
                public=False,
                name='Traconin edustuspaitatilaus 2019',
                name_genitive='Traconin edustuspaitatilauksen',
                name_illative='Traconin edustuspaitatilaukseen',
                name_inessive='Traconin edustuspaitatilauksen',
                homepage_url='http://ry.tracon.fi/',
                organization=organization,
                start_time=datetime(2019, 9, 6, 10, 0, tzinfo=tz),
                end_time=datetime(2019, 9, 8, 22, 0, tzinfo=tz),
                venue=venue,
            )
        )

        tickets_admin_group, pos_access_group = TicketsEventMeta.get_or_create_groups(event, ['admins', 'pos'])
        payments_admin_group, = PaymentsEventMeta.get_or_create_groups(event, ['admins'])

        tracon_payments = PaymentsEventMeta.objects.get(event__slug='tracon2019')
        PaymentsEventMeta.objects.get_or_create(
            event=event,
            defaults=dict(
                admin_group=payments_admin_group,
                checkout_delivery_date='20190906',
                checkout_merchant=tracon_payments.checkout_merchant,
                checkout_password=tracon_payments.checkout_password,
            ),
        )

        defaults = dict(
            admin_group=tickets_admin_group,
            pos_access_group=pos_access_group,
            due_days=14,
            shipping_and_handling_cents=0,
            reference_number_template="2019{:06d}",
            contact_email='Traconin lipunmyynti <liput@tracon.fi>',
            front_page_text=(
                "<h2>Tervetuloa tilaamaan Traconin edustustuotteita!</h2>"
                "<p>Omavastuuosuus maksetaan suomalaisilla verkkopankkitunnuksilla heti tilauksen yhteydessä.</p>"
                "<p>Huomaathan, että vaikka Toimitusosoite-vaiheessa kysytään postiosoitetta, edustustuotteita ei pääsääntöisesti postiteta. Edustustuotteita jaetaan conitean tilaisuuksissa kuten workshopeissa, ja voit sopia noudosta myös muiden tapahtumien edustuspöydiltä. Viimeistään saat edustustuotteesi Traconissa.</p>"
                "<p><strong>TÄRKEÄÄ:</strong> Lue kaikki ohjeet huolellisesti, sillä sovellamme verkkokauppaa sellaiseen käyttötarkoitukseen johon sitä ei ole suunniteltu. Erityisesti nimikoinnin ohjeet seuraavalla sivulla ovat epäintuitiiviset. Sori siitä.</p>"
            ),
        )

        if settings.DEBUG:
            t = now()
            defaults.update(
                ticket_sales_starts=t - timedelta(days=60),
                ticket_sales_ends=t + timedelta(days=60),
            )

        meta, unused = TicketsEventMeta.objects.get_or_create(event=event, defaults=defaults)

        def limit_group(description, limit):
            limit_group, unused = LimitGroup.objects.get_or_create(
                event=event,
                description=description,
                defaults=dict(limit=limit),
            )

            return limit_group

        def limit_group(description, limit):
            limit_group, unused = LimitGroup.objects.get_or_create(
                event=event,
                description=description,
                defaults=dict(limit=limit),
            )

            return limit_group

        for index, product_info in enumerate([
            dict(
                name='Kauluspaita tai huppari',
                description=(
                    'Teknisistä syistä kauluspaidat ja hupparit on tässä niputettu samaan tuotteeseen. '
                    'Syötä tässä lukumääräksi haluamiesi paitojen ja hupparien yhteenlaskettu määrä. '
                    'Pääset seuraavassa vaiheessa valitsemaan, tilaatko paidan, hupparin vai molemmat, '
                    'sekä valitsemaan värit ja koot.'
                ),
                limit_groups=[
                    limit_group('Edustustuotteet', 9999),
                ],
                price_cents=1500,
                requires_shipping=False,
                electronic_ticket=False,
                requires_shirt_size=True,
                available=True,
            ),
            dict(
                name='Nimikointi',
                description=(
                    'Jos haluat kauluspaitasi tai hupparisi nimikoituna, lisää tilaukseesi yhtä monta tätä tuotetta kuin tilaat huppareita tai kauluspaitoja.</p>'
                    '<p><strong>TÄRKEÄÄ:</strong> Jos tilaat nimikointeja, nimikointien määrän täytyy olla sama kuin tilattujen hupparien/kauluspaitojen määrän. '
                    'Verkkokauppa ei tarkista tätä automaattisesti, joten ole huolellinen tai aiheutat lisätyötä. '
                    'Jos haluat tilata sekä nimikoituja että nimikoimattomia tuotteita, tee niistä erilliset tilaukset. </p>'
                    '<p><strong>Syötä nimikointiteksti Toimitusosoite-vaiheessa Etunimi-kenttään, vaikkei se olisi oikea etunimesi.</strong>'
                ),
                limit_groups=[
                    limit_group('Nimikoinnit', 9999),
                ],
                price_cents=500,
                requires_shipping=False,
                electronic_ticket=False,
                requires_shirt_size=False,
                available=True,
            ),
        ]):
            name = product_info.pop('name')
            limit_groups = product_info.pop('limit_groups')

            product, unused = Product.objects.get_or_create(
                event=event,
                name=name,
                defaults=dict(product_info, ordering=index * 10),
            )

            if not product.limit_groups.exists():
                product.limit_groups.set(limit_groups)
                product.save()

        for shirt_type_slug, shirt_type_name, shirt_size_names in [
            ('huppari-musta', 'Huppari, musta', ['XS', 'S', 'M', 'L', 'XL', '2XL', '3XL']),
            ('huppari-punainen', 'Huppari, punainen', ['XS', 'S', 'M', 'L', 'XL', '2XL', '3XL']),
            ('kauluspaita-miehet', 'Miesten kauluspaita, musta', ['S', 'M', 'L', 'XL', '2XL', '3XL', '4XL']),
            ('kauluspaita-naiset', 'Naisten kauluspaita, musta', ['S', 'M', 'L', 'XL', '2XL', '3XL', '4XL']),
        ]:
            shirt_type, created = ShirtType.objects.get_or_create(
                event=event,
                slug=shirt_type_slug,
                defaults=dict(
                    name=shirt_type_name,
                ),
            )

            if created:
                for shirt_size_name in shirt_size_names:
                    ShirtSize.objects.get_or_create(
                        type=shirt_type,
                        slug=shirt_size_name,
                        defaults=dict(
                            name=shirt_size_name,
                        ),
                    )
