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
    def __init__(self):
        self._ordering = 0

    def get_ordering_number(self):
        self._ordering += 10
        return self._ordering

    def setup(self, test=False):
        self.test = test
        self.tz = tzlocal()
        self.setup_core()
        self.setup_labour()
        self.setup_tickets()
        self.setup_payments()
        self.setup_programme()

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

    def setup_labour(self):
        from core.models import Person
        from labour.models import (
            AlternativeSignupForm,
            InfoLink,
            Job,
            JobCategory,
            LabourEventMeta,
            Perk,
            PersonnelClass,
            Qualification,
            WorkPeriod,
        )
        from ...models import SignupExtra, SpecialDiet, Night
        from django.contrib.contenttypes.models import ContentType

        labour_admin_group, = LabourEventMeta.get_or_create_groups(self.event, ['admins'])

        if self.test:
            from core.models import Person
            person, unused = Person.get_or_create_dummy()
            labour_admin_group.user_set.add(person.user)

        content_type = ContentType.objects.get_for_model(SignupExtra)

        labour_event_meta_defaults = dict(
            signup_extra_content_type=content_type,
            work_begins=datetime(2015, 7, 10, 12, 0, tzinfo=self.tz),
            work_ends=datetime(2015, 7, 12, 22, 0, tzinfo=self.tz),
            admin_group=labour_admin_group,
            contact_email='Animeconin työvoimatiimi <tyovoima@animecon.fi>',
        )

        if self.test:
            t = now()
            labour_event_meta_defaults.update(
                registration_opens=t - timedelta(days=60),
                registration_closes=t + timedelta(days=60),
            )
        else:
            # TODO once we know when the registration opens
            # labour_event_meta_defaults.update(
            #     registration_opens=datetime(2014, 3, 1, 0, 0, tzinfo=self.tz),
            #     registration_closes=datetime(2014, 8, 1, 0, 0, tzinfo=self.tz),
            # )
            pass

        labour_event_meta, unused = LabourEventMeta.objects.get_or_create(
            event=self.event,
            defaults=labour_event_meta_defaults,
        )

        for pc_name, pc_slug, pc_app_label in [
            (u'Conitea', 'conitea', 'labour'),
            (u'Työvoima', 'tyovoima', 'labour'),
            (u'Järjestyksenvalvoja', 'jv', 'labour'),
            (u'Ohjelmanjärjestäjä', 'ohjelma', 'programme'),
            (u'Kunniavieras', 'goh', 'programme'), # tervetullut muttei kutsuta automaattiviestillä
            (u'Tulkki', 'tulkki', 'labour'),
            (u'Media', 'media', 'badges'),
            (u'Myyjä', 'myyja', 'badges'),
        ]:
            personnel_class, created = PersonnelClass.objects.get_or_create(
                event=self.event,
                slug=pc_slug,
                defaults=dict(
                    name=pc_name,
                    app_label=pc_app_label,
                    priority=self.get_ordering_number(),
                ),
            )

        tyovoima = PersonnelClass.objects.get(event=self.event, slug='tyovoima')
        jv = PersonnelClass.objects.get(event=self.event, slug='jv')
        conitea = PersonnelClass.objects.get(event=self.event, slug='conitea')
        ohjelma = PersonnelClass.objects.get(event=self.event, slug='ohjelma')

        for name, description, pcs in [
            (u'Conitea', u'Tapahtuman järjestelytoimikunnan eli conitean jäsen', [conitea]),

            (u'Narikka', u'Narikassa ja isotavara- eli asenarikassa säilytetään tapahtuman aikana kävijöiden omaisuutta. Tehtävä ei vaadi erikoisosaamista.', [tyovoima]),
            (u'Info', u'Infopisteen henkilökunta vastaa kävijöiden kysymyksiin ja ratkaisee heidän ongelmiaan tapahtuman paikana. Tehtävä edellyttää asiakaspalveluasennetta, tervettä järkeä ja ongelmanratkaisukykyä.', [tyovoima]),
            (u'Siivous', u'Tapahtumapaikan siistinä pitäminen tapahtuman aikana.', [tyovoima]),
            (u'Yleisvänkäri', u'Sekalaisia tehtäviä laidasta laitaan, jotka eivät vaadi erikoisosaamista. Voit halutessasi kirjata lisätietoihin, mitä osaat ja haluaisit tehdä.', [tyovoima]),
            (u'Majoitusvalvoja', u'Huolehtivat lattiamajoituspaikkojen pyörittämisestä yöaikaan. Työvuoroja myös molempina öinä.', [tyovoima]),
            (u'Myynti', u'Pääsylippujen myyntiä sekä lippujen tarkastamista. Myyjiltä edellytetään täysi-ikäisyyttä, asiakaspalveluhenkeä ja huolellisuutta rahankäsittelyssä. Vuoroja myös perjantaina.', [tyovoima]),
            (u'Green room', u'Työvoiman ruokahuolto green roomissa. Hygieniapassi suositeltava.', [tyovoima]),
            (u'Kirjasto', u'Mangakirjaston virkailijana toimimista.', [tyovoima]),
            (u'Ohjelma-avustaja', u'Lautapelien pyörittämistä, karaoken valvontaa, cosplay-kisaajien avustamista. Kerro Vapaa alue -kohdassa tarkemmin, mitä haluaisit tehdä. Huom! Puheohjelmasalien vänkäreiltä toivotaan AV-tekniikan osaamista.', [tyovoima]),
            (u'Kasaus ja purku', u'Kalusteiden siirtelyä & opasteiden kiinnittämistä. Ei vaadi erikoisosaamista. Työvuoroja myös jo pe sekä su conin sulkeuduttua, kerro lisätiedoissa jos voit osallistua näihin.', [tyovoima]),
            (u'Järjestyksenvalvoja', u'Kävijöiden turvallisuuden valvominen conipaikalla ja yömajoituksessa. Edellyttää voimassa olevaa JV-korttia ja asiakaspalveluasennetta. HUOM! Et voi valita tätä tehtävää hakemukseesi, ellet ole täyttänyt tietoihisi JV-kortin numeroa (oikealta ylhäältä oma nimesi &gt; Pätevyydet).', [jv]),
            (u'Kortiton järjestyksenvalvoja', u'Kävijöiden turvallisuuden valvominen conipaikalla ja yömajoituksessa. HUOM! Tähän tehtävään hakeminen edellyttää henkilötunnuksen syöttämistä sille varattuun kenttään.', [jv]),

            (u'Erikoistehtävä', u'Mikäli olet sopinut erikseen työtehtävistä ja/tai sinut on ohjeistettu täyttämään lomake, valitse tämä ja kerro tarkemmin Vapaa alue -kentässä mihin tehtävään ja kenen toimesta sinut on valittu.', [tyovoima]),

            (u'Ohjelmanpitäjä', u'Luennon tai muun vaativan ohjelmanumeron pitäjä', [ohjelma]),
        ]:
            job_category, created = JobCategory.objects.get_or_create(
                event=self.event,
                name=name,
                defaults=dict(
                    description=description,
                    slug=slugify(name),
                )
            )

            if created:
                job_category.personnel_classes = pcs
                job_category.save()

        labour_event_meta.create_groups()

        for name in [u'Conitea']:
            JobCategory.objects.filter(event=self.event, name=name).update(public=False)

        for jc_name, qualification_name in [
            (u'Järjestyksenvalvoja', u'JV-kortti'),
            # (u'Green room', u'Hygieniapassi'),
        ]:
            jc = JobCategory.objects.get(event=self.event, name=jc_name)
            qual = Qualification.objects.get(name=qualification_name)

        # TODO
        period_length = timedelta(hours=8)
        for period_description, period_start in [
            ("Perjantain kasaus (pe klo 12–21)", None),
            ("Lauantain aamuvuoro (la klo 08–14)", None),
            ("Lauantain iltapäivävuoro (la klo 14–20)", None),
            ("Lauantain iltavuoro (la klo 20–02)", None),
            ("Lauantai–sunnuntai-yövuoro (su klo 02–08)", None),
            ("Sunnuntain aamuvuoro (su klo 08–14)", None),
            ("Sunnuntain iltapäivävuoro ja purku (su klo 14–20)", None),
        ]:
            WorkPeriod.objects.get_or_create(
                event=self.event,
                description=period_description,
                defaults=dict(
                    start_time=period_start,
                    end_time=(period_start + period_length) if period_start else None,
                )
            )

        for diet_name in [
            u'Gluteeniton',
            u'Laktoositon',
            u'Maidoton',
            u'Vegaaninen',
            u'Lakto-ovo-vegaaninen',
        ]:
            SpecialDiet.objects.get_or_create(name=diet_name)

        for night in [
            u'Perjantain ja lauantain välinen yö',
            u'Lauantain ja sunnuntain välinen yö',
        ]:
            Night.objects.get_or_create(name=night)

        AlternativeSignupForm.objects.get_or_create(
            event=self.event,
            slug=u'conitea',
            defaults=dict(
                title=u'Conitean ilmoittautumislomake',
                signup_form_class_path='events.animecon2015.forms:OrganizerSignupForm',
                signup_extra_form_class_path='events.animecon2015.forms:OrganizerSignupExtraForm',
                active_from=datetime(2015, 3, 3, 18, 0, 0, tzinfo=self.tz),
                active_until=datetime(2015, 11, 22, 23, 59, 59, tzinfo=self.tz),
            ),
        )

        for wiki_space, link_title, link_group in [
            ('ACONWORK', 'Työvoimawiki', 'accepted'),
        ]:
            InfoLink.objects.get_or_create(
                event=self.event,
                title=link_title,
                defaults=dict(
                    url='https://confluence.tracon.fi/display/{wiki_space}'.format(wiki_space=wiki_space),
                    group=labour_event_meta.get_group(link_group),
                )
            )

    def setup_tickets(self):
        from tickets.models import TicketsEventMeta, LimitGroup, Product

        tickets_admin_group, = TicketsEventMeta.get_or_create_groups(self.event, ['admins'])

        defaults = dict(
            admin_group=tickets_admin_group,
            due_days=14,
            shipping_and_handling_cents=120,
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
                u"toimituksen ulkomaille, ole hyvä ja ota sähköpostitse yhteyttä: <em>liput@animecon.fi</em>"
        )

        if self.test:
            t = now()
            defaults.update(
                ticket_sales_starts=t - timedelta(days=60),
                ticket_sales_ends=t + timedelta(days=60),
            )
        else:
            defaults.update(
                ticket_sales_starts=datetime(2015, 3, 4, 18, 0, tzinfo=self.tz),
                ticket_sales_ends=datetime(2015, 6, 28, 18, 0, tzinfo=self.tz),
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
                name=u'Animecon 2015 -pääsylippu',
                description=u'Viikonloppuranneke Kuopiossa järjestettävään Animecon-tapahtumaan. Huom. myynnissä vain viikonloppurannekkeita. Lippu lähetetään postitse.',
                limit_groups=[
                    limit_group('Pääsyliput', 3000),
                ],
                price_cents=1600,
                requires_shipping=True,
                electronic_ticket=False,
                available=True,
                ordering=self.get_ordering_number(),
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
                ordering=self.get_ordering_number(),
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
                ordering=self.get_ordering_number(),
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
                ordering=self.get_ordering_number(),
            ),
            dict(
                name=u'Animecon 2015 -konserttilippu',
                description=u'Lippu Animeconin konserttiin. Mikäli tarvitset pyörätuolipaikkaa, otathan ennen ostoa yhteyttä <em>liput@animecon.fi</em>, jotta voimme varmistaa paikkatilanteen.',
                limit_groups=[
                    limit_group('Konserttiliput', 820),
                ],
                price_cents=500,
                requires_shipping=True,
                electronic_ticket=False,
                available=True,
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

        # v5
        if not meta.print_logo_path:
            meta.print_logo_path = mkpath('static', 'images', 'animecon.png')
            meta.print_logo_width_mm = 30
            meta.print_logo_height_mm = 30
            meta.save()

    def setup_payments(self):
        from payments.models import PaymentsEventMeta
        PaymentsEventMeta.get_or_create_dummy(event=self.event)

    def setup_programme(self):
        from programme.models import (
            Category,
            Programme,
            ProgrammeEventMeta,
            Role,
            Room,
            SpecialStartTime,
            TimeBlock,
            View,
        )

        programme_admin_group, = ProgrammeEventMeta.get_or_create_groups(self.event, ['admins'])
        programme_event_meta, unused = ProgrammeEventMeta.objects.get_or_create(event=self.event, defaults=dict(
            public=False,
            admin_group=programme_admin_group,
            contact_email='Animeconin ohjelmatiimi <ohjelma@animecon.fi>',
        ))

        for room_name in [
            u'Konserttisali',
            u'Kamarimusiikkisali',
            u'Auditorio',
            u'Jousisto',
            u'Luokka 210',
        ]:
            Room.objects.get_or_create(
                venue=self.venue,
                name=room_name,
                defaults=dict(
                    order=self.get_ordering_number()
                )
            )

        role, unused = Role.objects.get_or_create(
            title=u'Ohjelmanjärjestäjä',
            defaults=dict(
                is_default=True,
                require_contact_info=True,
            )
        )

        have_categories = Category.objects.filter(event=self.event).exists()
        if not have_categories:
            for title, style in [
                (u'Anime ja manga', u'anime'),
                (u'Cosplay', u'cosplay'),
                (u'Paja', u'miitti'),
                (u'Muu ohjelma', u'muu'),
                (u'Kunniavieras', u'rope'),
            ]:
                Category.objects.get_or_create(
                    event=self.event,
                    style=style,
                    defaults=dict(
                        title=title,
                    )
                )

        if self.test:
            # create some test programme
            Programme.objects.get_or_create(
                category=Category.objects.get(title='Anime ja manga', event=self.event),
                title='Yaoi-paneeli',
                defaults=dict(
                    description='Kika-kika tirsk',
                )
            )

        for start_time, end_time in [
            (
                self.event.start_time.replace(hour=10, minute=0),
                self.event.start_time.replace(hour=20, minute=0),
            ),
            (
                self.event.end_time.replace(hour=10, minute=0),
                self.event.end_time,
            ),
        ]:
            TimeBlock.objects.get_or_create(
                event=self.event,
                start_time=start_time,
                defaults=dict(
                    end_time=end_time
                )
            )

        SpecialStartTime.objects.get_or_create(
            event=self.event,
            start_time=self.event.start_time,
        )

        for view_name, room_names in [
            (u'Pääohjelmatilat', [
                u'Konserttisali',
                u'Kamarimusiikkisali',
                u'Auditorio',
                u'Jousisto',
                u'Luokka 210',
            ]),
        ]:
            rooms = [Room.objects.get(name__iexact=room_name, venue=self.venue)
                for room_name in room_names]

            view, created = View.objects.get_or_create(event=self.event, name=view_name)

            if created:
                view.rooms = rooms
                view.save()


class Command(BaseCommand):
    args = ''
    help = 'Setup animecon2015 specific stuff'

    def handle(self, *args, **opts):
        Setup().setup(test=settings.DEBUG)
