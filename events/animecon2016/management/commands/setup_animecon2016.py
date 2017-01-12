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
        self.setup_badges()

    def setup_core(self):
        from core.models import Venue, Event

        self.venue, unused = Venue.objects.get_or_create(name='Jyväskylän Paviljonki', defaults=dict(
            name_inessive='Jyväskylän Paviljongissa',
        ))
        self.event, unused = Event.objects.get_or_create(slug='animecon2016', defaults=dict(
            name='Animecon 2016',
            name_genitive='Animecon 2016 -tapahtuman',
            name_illative='Animecon 2016 -tapahtumaan',
            name_inessive='Animecon 2016 -tapahtumassa',
            homepage_url='http://2016.animecon.fi',
            organization_name='Nekocon ry',
            organization_url='http://animecon.fi',
            start_time=datetime(2016, 7, 9, 9, 30, tzinfo=self.tz),
            end_time=datetime(2016, 7, 10, 17, 0, tzinfo=self.tz),
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
            work_begins=self.event.start_time - timedelta(days=1),
            work_ends=self.event.end_time + timedelta(hours=4),
            admin_group=labour_admin_group,
            contact_email='Animeconin työvoimatiimi <tyovoima@animecon.fi>',
        )

        if self.test:
            t = now()
            labour_event_meta_defaults.update(
                registration_opens=t - timedelta(days=60),
                registration_closes=t + timedelta(days=60),
            )

        labour_event_meta, unused = LabourEventMeta.objects.get_or_create(
            event=self.event,
            defaults=labour_event_meta_defaults,
        )

        for pc_name, pc_slug, pc_app_label in [
            ('Conitea', 'conitea', 'labour'),
            ('Työvoima', 'tyovoima', 'labour'),
            ('Järjestyksenvalvoja', 'jv', 'labour'),
            ('Ohjelmanjärjestäjä', 'ohjelma', 'programme'),
            ('Kunniavieras', 'goh', 'programme'), # tervetullut muttei kutsuta automaattiviestillä
            ('Tulkki', 'tulkki', 'labour'),
            ('Media', 'media', 'badges'),
            ('Myyjä', 'myyja', 'badges'),
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
            ('Conitea', 'Tapahtuman järjestelytoimikunnan eli conitean jäsen', [conitea]),

            ('Narikka', 'Narikassa ja isotavara- eli asenarikassa säilytetään tapahtuman aikana kävijöiden omaisuutta. Tehtävä ei vaadi erikoisosaamista.', [tyovoima]),
            ('Info', 'Infopisteen henkilökunta vastaa kävijöiden kysymyksiin ja ratkaisee heidän ongelmiaan tapahtuman paikana. Tehtävä edellyttää asiakaspalveluasennetta, tervettä järkeä ja ongelmanratkaisukykyä.', [tyovoima]),
            ('Siivous', 'Tapahtumapaikan siistinä pitäminen tapahtuman aikana.', [tyovoima]),
            ('Yleisvänkäri', 'Sekalaisia tehtäviä laidasta laitaan, jotka eivät vaadi erikoisosaamista. Voit halutessasi kirjata lisätietoihin, mitä osaat ja haluaisit tehdä.', [tyovoima]),
            ('Majoitusvalvoja', 'Huolehtivat lattiamajoituspaikkojen pyörittämisestä yöaikaan. Työvuoroja myös molempina öinä.', [tyovoima]),
            ('Myynti', 'Pääsylippujen myyntiä sekä lippujen tarkastamista. Myyjiltä edellytetään täysi-ikäisyyttä, asiakaspalveluhenkeä ja huolellisuutta rahankäsittelyssä. Vuoroja myös perjantaina.', [tyovoima]),
            ('Green room', 'Työvoiman ruokahuolto green roomissa. Hygieniapassi suositeltava.', [tyovoima]),
            ('Kirjasto', 'Mangakirjaston virkailijana toimimista.', [tyovoima]),
            ('Ohjelma-avustaja', 'Lautapelien pyörittämistä, karaoken valvontaa, cosplay-kisaajien avustamista. Kerro Vapaa alue -kohdassa tarkemmin, mitä haluaisit tehdä. Huom! Puheohjelmasalien vänkäreiltä toivotaan AV-tekniikan osaamista.', [tyovoima]),
            ('Kasaus ja purku', 'Kalusteiden siirtelyä & opasteiden kiinnittämistä. Ei vaadi erikoisosaamista. Työvuoroja myös jo pe sekä su conin sulkeuduttua, kerro lisätiedoissa jos voit osallistua näihin.', [tyovoima]),
            ('Järjestyksenvalvoja', 'Kävijöiden turvallisuuden valvominen conipaikalla ja yömajoituksessa. Edellyttää voimassa olevaa JV-korttia ja asiakaspalveluasennetta. HUOM! Et voi valita tätä tehtävää hakemukseesi, ellet ole täyttänyt tietoihisi JV-kortin numeroa (oikealta ylhäältä oma nimesi &gt; Pätevyydet).', [jv]),
            ('Kortiton järjestyksenvalvoja', 'Kävijöiden turvallisuuden valvominen conipaikalla ja yömajoituksessa. HUOM! Tähän tehtävään hakeminen edellyttää henkilötunnuksen syöttämistä sille varattuun kenttään.', [jv]),

            ('Erikoistehtävä', 'Mikäli olet sopinut erikseen työtehtävistä ja/tai sinut on ohjeistettu täyttämään lomake, valitse tämä ja kerro tarkemmin Vapaa alue -kentässä mihin tehtävään ja kenen toimesta sinut on valittu.', [tyovoima]),

            ('Ohjelmanpitäjä', 'Luennon tai muun vaativan ohjelmanumeron pitäjä', [ohjelma]),
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
            ('Järjestyksenvalvoja', 'JV-kortti'),
            # ('Green room', 'Hygieniapassi'),
        ]:
            jc = JobCategory.objects.get(event=self.event, name=jc_name)
            qual = Qualification.objects.get(name=qualification_name)

        for diet_name in [
            'Gluteeniton',
            'Laktoositon',
            'Maidoton',
            'Vegaaninen',
            'Lakto-ovo-vegetaristinen',
        ]:
            SpecialDiet.objects.get_or_create(name=diet_name)

        for night in [
            'Perjantain ja lauantain välinen yö',
            'Lauantain ja sunnuntain välinen yö',
        ]:
            Night.objects.get_or_create(name=night)

        AlternativeSignupForm.objects.get_or_create(
            event=self.event,
            slug='conitea',
            defaults=dict(
                title='Conitean ilmoittautumislomake',
                signup_form_class_path='events.animecon2016.forms:OrganizerSignupForm',
                signup_extra_form_class_path='events.animecon2016.forms:OrganizerSignupExtraForm',
                active_from=datetime(2016, 2, 21, 18, 0, 0, tzinfo=self.tz),
                active_until=self.event.start_time,
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
            reference_number_template="2016{:05d}",
            contact_email='Animecon 2016 <liput@animecon.fi>',
            plain_contact_email='liput@animecon.fi',
            ticket_free_text="Tämä on sähköinen lippusi Animecon 2016 -tapahtumaan. Sähköinen lippu vaihdetaan rannekkeeseen\n"
                "lipunvaihtopisteessä saapuessasi tapahtumaan. Voit tulostaa tämän lipun tai näyttää sen\n"
                "älypuhelimen tai tablettitietokoneen näytöltä. Mikäli kumpikaan näistä ei ole mahdollista, ota ylös\n"
                "kunkin viivakoodin alla oleva neljästä tai viidestä sanasta koostuva Kissakoodi ja ilmoita se\n"
                "lipunvaihtopisteessä.\n\n"
                "Tervetuloa Animecon 2016 -tapahtumaan!",
            front_page_text="<h2>Tervetuloa ostamaan pääsylippuja Animecon 2016 -tapahtumaan!</h2>"
                "<p>Liput maksetaan suomalaisilla verkkopankkitunnuksilla heti tilauksen yhteydessä.</p>"
                "<p>Lue lisää tapahtumasta <a href='http://2016.animecon.fi'>Animecon 2016 -tapahtuman kotisivuilta</a>.</p>"
                "<p>Huom! Tämä verkkokauppa palvelee ainoastaan asiakkaita, joilla on osoite Suomessa. Mikäli tarvitset "
                "toimituksen ulkomaille, ole hyvä ja ota sähköpostitse yhteyttä: <em>liput@animecon.fi</em>"
        )

        if self.test:
            t = now()
            defaults.update(
                ticket_sales_starts=t - timedelta(days=60),
                ticket_sales_ends=t + timedelta(days=60),
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
                name='Animecon 2016 -pääsylippu',
                description='Viikonloppuranneke Kuopiossa järjestettävään Animecon-tapahtumaan. Huom. myynnissä vain viikonloppurannekkeita. Lippu on PDF-muotoinen e-lippu, joka vaihdetaan rannekkeeseen tapahtumaan saavuttaessa.',
                limit_groups=[
                    limit_group('Pääsyliput', 3300),
                ],
                price_cents=2000,
                requires_shipping=False,
                electronic_ticket=True,
                available=True,
                ordering=self.get_ordering_number(),
            ),
            dict(
                name='Lattiamajoitus Viitaniemen koululla pe-la-yöksi',
                description='Lattiamajoituspaikka 8.-9.7.2016 välisenä yönä Viitaniemen koululla. Luethan ohjeet majoittumiseen Animeconin nettisivuilta. Jos maksat muitakin henkilöitä kuin itsesi, niin ilmoitathan kaikkien majoittujien yhteystiedot (nimi, puhelinnumero, sähköposti) lisätiedoissa. Emme lähetä lattiamajoituksesta erillistä lippua.',
                limit_groups=[
                    limit_group('Majoitus Viitaniemi pe-la', 200),
                ],
                price_cents=1000,
                requires_shipping=False,
                electronic_ticket=False,
                requires_accommodation_information=True,
                available=True,
                ordering=self.get_ordering_number(),
            ),
            dict(
                name='Lattiamajoitus Viitaniemen koululla la-su-yöksi',
                description='Lattiamajoituspaikka 9.-10.7.2016 välisenä yönä Viitaniemen koululla. Luethan ohjeet majoittumiseen Animeconin nettisivuilta. Jos maksat muitakin majoittujia kuin itsesi, niin ilmoitathan kaikkien majoittujien yhteystiedot (nimi, puhelinnumero, sähköposti) lisätiedoissa. Emme lähetä lattiamajoituksesta erillistä lippua.',
                limit_groups=[
                    limit_group('Majoitus Viitaniemi la-su', 200),
                ],
                price_cents=1000,
                requires_shipping=False,
                electronic_ticket=False,
                requires_accommodation_information=True,
                available=True,
                ordering=self.get_ordering_number(),
            ),
            dict(
                name='Aamupala Viitaniemen koululla lauantaiaamuna',
                description='Aamupala Viitaniemen koululla lauantaiaamuna 9.7.2016. Ilmoitathan erityisruokavalioista ja allergioista etukäteen. Jos olet varannut aamiaisen myös muille kuin itsellesi, niin ilmoitathan henkilöiden nimet lisätiedoissa.',
                limit_groups=[
                    limit_group('Aamupala Viitaniemi la', 200),
                ],
                price_cents=350,
                requires_shipping=False,
                electronic_ticket=False,
                requires_accommodation_information=True,
                available=True,
                ordering=self.get_ordering_number(),
            ),
            dict(
                name='Aamupala Viitaniemen koululla sunnuntaiaamuna',
                description='Aamupala Viitaniemen koululla sunnuntai-aamuna 10.7.2016. Ilmoitathan erityisruokavalioista ja allergioista etukäteen. Jos olet varannut aamiaisen myös muille kuin itsellesi, niin ilmoitathan henkilöiden nimet lisätiedoissa.',
                limit_groups=[
                    limit_group('Aamupala Viitaniemi su', 200),
                ],
                price_cents=350,
                requires_shipping=False,
                electronic_ticket=False,
                requires_accommodation_information=True,
                available=True,
                ordering=self.get_ordering_number(),
            ),
            dict(
                name='Lattiamajoituspaikka Jyväskylän Tanssiopistolla perjantai-lauantai-yöksi',
                description='Lattiamajoituspaikka 8.-9.7.2016 välisenä yönä Jyväskylän Tanssiopistolla. Luethan ohjeet majoittumiseen Animeconin nettisivuilta. Jos maksat muitakin majoittujia kuin itsesi, niin ilmoitathan kaikkien majoittujien yhteystiedot (nimi, puhelinnumero, sähköposti) lisätiedoissa. Emme lähetä lattiamajoituksesta erillistä lippua',
                limit_groups=[
                    limit_group('Majoitus Tanssiopisto pe-la', 118),
                ],
                price_cents=1000,
                requires_shipping=False,
                electronic_ticket=False,
                requires_accommodation_information=True,
                available=True,
                ordering=self.get_ordering_number(),
            ),
            dict(
                name='Lattiamajoituspaikka Jyväskylän Tanssiopistolla lauantai-sunnuntai-yöksi',
                description='Lattiamajoituspaikka 9.-10.7.2016 välisenä yönä Jyväskylän Tanssiopistolla. Luethan ohjeet majoittumiseen Animeconin nettisivuilta. Jos maksat muitakin majoittujia kuin itsesi, niin ilmoitathan kaikkien majoittujien yhteystiedot (nimi, puhelinnumero, sähköposti) lisätiedoissa. Emme lähetä lattiamajoituksesta erillistä lippua',
                limit_groups=[
                    limit_group('Majoitus Tanssiopisto la-su', 118),
                ],
                price_cents=1000,
                requires_shipping=False,
                electronic_ticket=False,
                requires_accommodation_information=True,
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
        # if not meta.print_logo_path:
        #     meta.print_logo_path = mkpath('static', 'images', 'animecon.png')
        #     meta.print_logo_width_mm = 30
        #     meta.print_logo_height_mm = 30
        #     meta.save()

    def setup_payments(self):
        from payments.models import PaymentsEventMeta
        PaymentsEventMeta.get_or_create_dummy(event=self.event)

    def setup_programme(self):
        from core.utils import full_hours_between
        from labour.models import PersonnelClass
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

        programme_admin_group, hosts_group = ProgrammeEventMeta.get_or_create_groups(self.event, ['admins', 'hosts'])
        programme_event_meta, unused = ProgrammeEventMeta.objects.get_or_create(event=self.event, defaults=dict(
            public=False,
            admin_group=programme_admin_group,
            contact_email='Animeconin ohjelmatiimi <ohjelma@animecon.fi>',
        ))

        for room_name in [
            'Auditorio',
            'Kabinetti',
            'Alvar',
            'Anton',
            'Elsi',
            'Felix',
            # 'Minna',
        ]:
            Room.objects.get_or_create(
                venue=self.venue,
                name=room_name,
                defaults=dict(
                    order=self.get_ordering_number()
                )
            )

        personnel_class = PersonnelClass.objects.get(event=self.event, slug='ohjelma')

        role, unused = Role.objects.get_or_create(
            personnel_class=personnel_class,
            title='Ohjelmanjärjestäjä',
            defaults=dict(
                is_default=True,
                require_contact_info=True,
            )
        )

        have_categories = Category.objects.filter(event=self.event).exists()
        if not have_categories:
            for title, style in [
                ('Anime ja manga', 'anime'),
                ('Cosplay', 'cosplay'),
                ('Paja', 'miitti'),
                ('Muu ohjelma', 'muu'),
                ('Kunniavieras', 'rope'),
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

        if not TimeBlock.objects.filter(event=self.event).exists():
            for start_time, end_time in [
                (
                    self.event.start_time.replace(hour=10, minute=0, tzinfo=self.tz),
                    self.event.start_time.replace(hour=20, minute=0, tzinfo=self.tz),
                ),
                (
                    self.event.end_time.replace(hour=10, minute=0, tzinfo=self.tz),
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

                for hour_start_time in full_hours_between(start_time, end_time)[:-1]:
                    SpecialStartTime.objects.get_or_create(
                        event=self.event,
                        start_time=hour_start_time.replace(minute=30)
                    )

        for view_name, room_names in [
            ('Pääohjelmatilat', [
                'Auditorio',
                'Kabinetti',
                'Alvar',
                'Anton',
                'Elsi',
                'Felix',
                # 'Minna',
            ]),
        ]:
            rooms = [Room.objects.get(name__iexact=room_name, venue=self.venue)
                for room_name in room_names]

            view, created = View.objects.get_or_create(event=self.event, name=view_name)

            if created:
                view.rooms = rooms
                view.save()

    def setup_badges(self):
        from badges.models import BadgesEventMeta

        badge_admin_group, = BadgesEventMeta.get_or_create_groups(self.event, ['admins'])
        meta, unused = BadgesEventMeta.objects.get_or_create(
            event=self.event,
            defaults=dict(
                admin_group=badge_admin_group,
                badge_layout='nick',
            )
        )


class Command(BaseCommand):
    args = ''
    help = 'Setup animecon2016 specific stuff'

    def handle(self, *args, **opts):
        Setup().setup(test=settings.DEBUG)
