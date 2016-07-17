# encoding: utf-8

from __future__ import unicode_literals

from datetime import datetime, timedelta

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.timezone import now

from dateutil.tz import tzlocal

from core.utils import slugify


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
        self.setup_badges()
        self.setup_tickets()
        self.setup_payments()
        self.setup_programme()
        self.setup_access()
        self.setup_sms()

    def setup_core(self):
        from core.models import Organization, Venue, Event

        self.organization, unused = Organization.objects.get_or_create(slug='tracon-ry', defaults=dict(
            name='Tracon ry',
            homepage_url='https://ry.tracon.fi',
        ))
        self.venue, unused = Venue.objects.get_or_create(name='Tampere-talo')
        self.event, unused = Event.objects.get_or_create(slug='tracon11', defaults=dict(
            name='Tracon (2016)',
            name_genitive='Traconin',
            name_illative='Traconiin',
            name_inessive='Traconissa',
            homepage_url='http://2016.tracon.fi',
            organization=self.organization,
            start_time=datetime(2016, 9, 3, 10, 0, tzinfo=self.tz),
            end_time=datetime(2016, 9, 4, 18, 0, tzinfo=self.tz),
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
            Survey,
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
            work_begins=datetime(2016, 9, 2, 8, 0, tzinfo=self.tz),
            work_ends=datetime(2016, 9, 4, 22, 0, tzinfo=self.tz),
            admin_group=labour_admin_group,
            contact_email='Traconin työvoimatiimi <tyovoima@tracon.fi>',
        )

        if self.test:
            t = now()
            labour_event_meta_defaults.update(
                registration_opens=t - timedelta(days=60),
                registration_closes=t + timedelta(days=60),
            )
        else:
            pass

        labour_event_meta, unused = LabourEventMeta.objects.get_or_create(
            event=self.event,
            defaults=labour_event_meta_defaults,
        )

        self.afterparty_perk, unused = Perk.objects.get_or_create(
            event=self.event,
            slug='kaatajaiset',
            defaults=dict(
                name='Kaatajaiset',
            ),
        )

        fmh = PersonnelClass.objects.filter(event=self.event, slug='ylivankari')
        if fmh.exists():
            fmh.update(name='Vuorovastaava', slug='vuorovastaava')

        for pc_name, pc_slug, pc_app_label, pc_afterparty in [
            ('Conitea', 'conitea', 'labour', True),
            ('Vuorovastaava', 'vuorovastaava', 'labour', True),
            ('Työvoima', 'tyovoima', 'labour', True),
            ('Ohjelma', 'ohjelma', 'programme', True),
            ('Ohjelma 2. luokka', 'ohjelma-2lk', 'programme', False),
            ('Ohjelma 3. luokka', 'ohjelma-3lk', 'programme', False),
            ('Guest of Honour', 'goh', 'programme', False), # tervetullut muttei kutsuta automaattiviestillä
            ('Media', 'media', 'badges', False),
            ('Myyjä', 'myyja', 'badges', False),
            ('Vieras', 'vieras', 'badges', False),
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

            if pc_afterparty and created:
                personnel_class.perks = [self.afterparty_perk]
                personnel_class.save()

        tyovoima = PersonnelClass.objects.get(event=self.event, slug='tyovoima')
        conitea = PersonnelClass.objects.get(event=self.event, slug='conitea')
        vuorovastaava = PersonnelClass.objects.get(event=self.event, slug='vuorovastaava')
        ohjelma = PersonnelClass.objects.get(event=self.event, slug='ohjelma')

        for jc_data in [
            ('Conitea', 'Tapahtuman järjestelytoimikunnan eli conitean jäsen', [conitea], [
                'Tapahtumavastaava',
                'Johtokeskuspäivystäjä',
            ]),

            ('Erikoistehtävä', 'Mikäli olet sopinut erikseen työtehtävistä ja/tai sinut on ohjeistettu täyttämään lomake, valitse tämä ja kerro tarkemmin Vapaa alue -kentässä mihin tehtävään ja kenen toimesta sinut on valittu.', [tyovoima, vuorovastaava]),
            ('Järjestyksenvalvoja', 'Kävijöiden turvallisuuden valvominen conipaikalla ja yömajoituksessa. Edellyttää voimassa olevaa JV-korttia ja asiakaspalveluasennetta. HUOM! Et voi valita tätä tehtävää hakemukseesi, ellet ole täyttänyt tietoihisi JV-kortin numeroa (oikealta ylhäältä oma nimesi &gt; Pätevyydet).', [tyovoima, vuorovastaava]),
            ('Kasaus ja purku', 'Kalusteiden siirtelyä & opasteiden kiinnittämistä. Ei vaadi erikoisosaamista. Työvuoroja myös jo pe sekä su conin sulkeuduttua, kerro lisätiedoissa jos voit osallistua näihin.', [tyovoima, vuorovastaava]),
            ('Logistiikka', 'Autokuskina toimimista ja tavaroiden/ihmisten hakua ja noutamista. B-luokan ajokortti vaaditaan. Työvuoroja myös perjantaille.', [tyovoima, vuorovastaava]),
            ('Majoitusvalvoja', 'Huolehtivat lattiamajoituspaikkojen pyörittämisestä yöaikaan. Työvuoroja myös molempina öinä.', [tyovoima, vuorovastaava]),
            ('Myynti', 'Pääsylippujen ja Tracon-oheistuotteiden myyntiä sekä lippujen tarkastamista. Myyjiltä edellytetään täysi-ikäisyyttä, asiakaspalveluhenkeä ja huolellisuutta rahankäsittelyssä. Vuoroja myös perjantaina.', [tyovoima, vuorovastaava]),
            ('Narikka', 'Narikassa ja isotavara- eli asenarikassa säilytetään tapahtuman aikana kävijöiden omaisuutta. Tehtävä ei vaadi erikoisosaamista.', [tyovoima, vuorovastaava]),
            ('Ohjelma-avustaja', 'Lautapelien pyörittämistä, karaoken valvontaa, cosplay-kisaajien avustamista. Kerro Vapaa alue -kohdassa tarkemmin, mitä haluaisit tehdä. Huom! Puheohjelmasalien vänkäreiltä toivotaan AV-tekniikan osaamista.', [tyovoima, vuorovastaava]),
            ('Green room', 'Työvoiman ruokahuolto green roomissa. Edellyttää hygieniapassia.', [tyovoima, vuorovastaava]),
            ('Taltiointi', 'Taltioinnin keskeisiin tehtäviin kuuluvat mm. saleissa esitettävien ohjelmanumeroiden videointi tapahtumassa ja editointi tapahtuman jälkeen. Lisäksi videoidaan dokumentaarisella otteella myös yleisesti tapahtumaa. Kerro Työkokemus-kentässä aiemmasta videokuvauskokemuksestasi (esim. linkkejä videogallerioihisi) sekä mitä haluaisit taltioinnissa tehdä.', [tyovoima, vuorovastaava]),
            ('Tekniikka', 'Salitekniikan (AV) ja tietotekniikan (tulostimet, lähiverkot, WLAN) nopeaa MacGyver-henkistä ongelmanratkaisua.', [tyovoima, vuorovastaava]),
            ('Valokuvaus', 'Valokuvaus tapahtuu pääasiassa kuvaajien omilla järjestelmäkameroilla. Tehtäviä voivat olla studiokuvaus, salikuvaus sekä yleinen valokuvaus. Kerro Työkokemus-kentässä aiemmasta valokuvauskokemuksestasi (esim. linkkejä kuvagallerioihisi) sekä mitä/missä haluaisit tapahtumassa valokuvata.', [tyovoima, vuorovastaava]),
            ('Yleisvänkäri', 'Sekalaisia tehtäviä laidasta laitaan, jotka eivät vaadi erikoisosaamista. Voit halutessasi kirjata lisätietoihin, mitä osaat ja haluaisit tehdä.', [tyovoima, vuorovastaava]),
            ('Info', 'Infopisteen henkilökunta vastaa kävijöiden kysymyksiin ja ratkaisee heidän ongelmiaan tapahtuman paikana. Tehtävä edellyttää asiakaspalveluasennetta, tervettä järkeä ja ongelmanratkaisukykyä.', [tyovoima, vuorovastaava]),

            # ('Ohjelmanpitäjä', 'Luennon tai muun vaativan ohjelmanumeron pitäjä', [ohjelma]),
        ]:
            if len(jc_data) == 3:
                name, description, pcs = jc_data
                job_names = []
            elif len(jc_data) == 4:
                name, description, pcs, job_names = jc_data
            else:
                raise ValueError("Length of jc_data must be 3 or 4")

            job_category, created = JobCategory.objects.get_or_create(
                event=self.event,
                slug=slugify(name),
                defaults=dict(
                    name=name,
                    description=description,
                )
            )

            if created:
                job_category.personnel_classes = pcs
                job_category.save()

            for job_name in job_names:
                job, created = Job.objects.get_or_create(
                    job_category=job_category,
                    slug=slugify(job_name),
                    defaults=dict(
                        title=job_name,
                    )
                )

        labour_event_meta.create_groups()

        for name in ['Conitea']:
            JobCategory.objects.filter(event=self.event, name=name).update(public=False)

        for jc_name, qualification_name in [
            ('Järjestyksenvalvoja', 'JV-kortti'),
            ('Logistiikka', 'Henkilöauton ajokortti (B)'),
            ('Green room', 'Hygieniapassi'),
        ]:
            jc = JobCategory.objects.get(event=self.event, name=jc_name)
            qual = Qualification.objects.get(name=qualification_name)
            if not jc.required_qualifications.exists():
                jc.required_qualifications = [qual]
                jc.save()

        event_starts = self.event.start_time
        event_ends = self.event.end_time
        work_begins = labour_event_meta_defaults['work_begins']
        period_length = timedelta(hours=8)
        for period_description, period_start in [
            ("Perjantain kasaustalkoot (pe klo 12-20)", work_begins.replace(hour=12)),
            ("Lauantain aamuvuoro (la klo 08-16)", event_starts.replace(hour=8)),
            ("Lauantain iltavuoro (la klo 16-24)", event_starts.replace(hour=16)),
            ("Lauantai-sunnuntai-yövuoro (su klo 00-08)", event_ends.replace(hour=0)),
            ("Sunnuntain aamuvuoro (su klo 08-16)", event_ends.replace(hour=8)),
            ("Sunnuntain iltavuoro (su klo 16-20)", event_ends.replace(hour=16)),
        ]:
            work_period, created = WorkPeriod.objects.get_or_create(
                event=self.event,
                description=period_description,
                defaults=dict(
                    start_time=period_start,
                    end_time=(period_start + period_length) if period_start else None,
                )
            )

            if work_period.start_time is None:
                work_period.start_time = period_start
                work_period.end_time = (period_start + period_length) if period_start else None
                work_period.save()

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
                signup_form_class_path='events.tracon11.forms:OrganizerSignupForm',
                signup_extra_form_class_path='events.tracon11.forms:OrganizerSignupExtraForm',
                active_from=datetime(2015, 9, 29, 15, 43, 0, tzinfo=self.tz),
                active_until=datetime(2016, 9, 4, 23, 59, 59, tzinfo=self.tz),
            ),
        )

        Survey.objects.get_or_create(
            event=self.event,
            slug='tyovuorotoiveet',
            defaults=dict(
                title='Työvuorotoiveet',
                description=(
                    'Tässä vaiheessa voit vaikuttaa työvuoroihisi. Jos saavut tapahtumaan vasta sen alkamisen '
                    'jälkeen tai sinun täytyy lähteä ennen tapahtuman loppumista, kerro se tässä. Lisäksi jos '
                    'tiedät ettet ole käytettävissä tiettyihin aikoihin tapahtuman aikana tai haluat esimerkiksi '
                    'nähdä jonkun ohjelmanumeron, kerro siitäkin. Työvuorotoiveiden toteutumista täysin ei voida '
                    'taata.'
                ),
                form_class_path='events.tracon11.forms:ShiftWishesSurvey',
                active_from=datetime(2016, 7, 16, 14, 13, 0, tzinfo=self.tz),
                active_until=datetime(2016, 7, 31, 23, 59, 59, tzinfo=self.tz),
            ),
        )

        for wiki_space, link_title, link_group in [
            ('TERA', 'Työvoimawiki', 'accepted'),
            ('INFO', 'Infowiki', 'info'),
        ]:
            InfoLink.objects.get_or_create(
                event=self.event,
                title=link_title,
                defaults=dict(
                    url='https://confluence.tracon.fi/display/{wiki_space}'.format(wiki_space=wiki_space),
                    group=labour_event_meta.get_group(link_group),
                )
            )

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

    def setup_tickets(self):
        from tickets.models import TicketsEventMeta, LimitGroup, Product

        tickets_admin_group, = TicketsEventMeta.get_or_create_groups(self.event, ['admins'])

        defaults = dict(
            admin_group=tickets_admin_group,
            due_days=14,
            shipping_and_handling_cents=0,
            reference_number_template="2016{:05d}",
            contact_email='Traconin lipunmyynti <liput@tracon.fi>',
            plain_contact_email='liput@tracon.fi',
            ticket_free_text="Tämä on sähköinen lippusi Tracon -tapahtumaan. Sähköinen lippu vaihdetaan rannekkeeseen\n"
                "lipunvaihtopisteessä saapuessasi tapahtumaan. Voit tulostaa tämän lipun tai näyttää sen\n"
                "älypuhelimen tai tablettitietokoneen näytöltä. Mikäli kumpikaan näistä ei ole mahdollista, ota ylös\n"
                "kunkin viivakoodin alla oleva neljästä tai viidestä sanasta koostuva sanakoodi ja ilmoita se\n"
                "lipunvaihtopisteessä.\n\n"
                "Tervetuloa Traconiin!",
            front_page_text="<h2>Tervetuloa ostamaan pääsylippuja Tracon -tapahtumaan!</h2>"
                "<p>Liput maksetaan suomalaisilla verkkopankkitunnuksilla heti tilauksen yhteydessä.</p>"
                "<p>Lue lisää tapahtumasta <a href='http://2016.tracon.fi'>Traconin kotisivuilta</a>.</p>",
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
                name='Viikonloppulippu',
                description='Voimassa koko viikonlopun ajan la klo 10 - su klo 18. Toimitetaan sähköpostitse PDF-tiedostona.',
                limit_groups=[
                    limit_group('Lauantain liput', 2900),
                    limit_group('Sunnuntain liput', 2900),
                ],
                price_cents=2500,
                requires_shipping=False,
                electronic_ticket=True,
                available=True,
                ordering=ordering(),
            ),
            dict(
                name='Lauantailippu',
                description='   Voimassa koko lauantaipäivän ajan la klo 10 - su klo 08. Toimitetaan sähköpostitse PDF-tiedostona.',
                limit_groups=[
                    limit_group('Lauantain liput', 2900),
                ],
                price_cents=1800,
                requires_shipping=False,
                electronic_ticket=True,
                available=True,
                ordering=ordering(),
            ),
            dict(
                name='Sunnuntailippu',
                description='   Voimassa koko sunnuntaipäivän ajan su klo 00 - su klo 18. Toimitetaan sähköpostitse PDF-tiedostona.',
                limit_groups=[
                    limit_group('Sunnuntain liput', 2900),
                ],
                price_cents=1500,
                requires_shipping=False,
                electronic_ticket=True,
                available=True,
                ordering=ordering(),
            ),
            dict(
                name='Iltabilelippu',
                description='Traconin iltabileet Pakkahuoneella lauantaina 3. syyskuuta 2016 kello 19–01. Esiintyjät julkistetaan lähempänä tapahtumaa. Ei edellytä pääsylippua Traconiin.',
                limit_groups=[
                    limit_group('Iltabileliput', 1300),
                ],
                price_cents=500,
                requires_shipping=False,
                electronic_ticket=True,
                available=True,
                ordering=ordering(),
            ),
            dict(
                name='Lattiamajoitus 1 yö pe-la - Aleksanterin koulu (sis. makuualusta)',
                description='Lattiamajoituspaikka perjantain ja lauantain väliseksi yöksi Aleksanterin koululta. Aleksanterin koulun majoituspaikat sisältävät makuualustan, joten sinun tarvitsee tuoda vain makuupussi.',
                limit_groups=[
                    limit_group('Majoitus Aleksanteri pe-la', 130),
                ],
                price_cents=1300,
                requires_shipping=False,
                requires_accommodation_information=True,
                electronic_ticket=False,
                available=True,
                ordering=ordering(),
            ),
            dict(
                name='Lattiamajoitus 1 yö la-su - Aleksanterin koulu (sis. makuualusta)',
                description='Lattiamajoituspaikka lauantain ja sunnuntain väliseksi yöksi Aleksanterin koululta. Aleksanterin koulun majoituspaikat sisältävät makuualustan, joten sinun tarvitsee tuoda vain makuupussi.',
                limit_groups=[
                    limit_group('Majoitus Aleksanteri la-su', 130),
                ],
                price_cents=1300,
                requires_shipping=False,
                requires_accommodation_information=True,
                electronic_ticket=False,
                available=True,
                ordering=ordering(),
            ),
            dict(
                name='Lattiamajoitus 1 yö pe-la - Pyynikin koulu (ei sis. makuualustaa)',
                description='Lattiamajoituspaikka lauantain ja sunnuntain väliseksi yöksi Pyynikin koululta. Pyynikin koulun majoituspaikat eivät sisällä makuualustaa, joten sinun tarvitsee tuoda makuupussi ja makuualusta tai patja.',
                limit_groups=[
                    limit_group('Majoitus Pyynikki pe-la', 120),
                ],
                price_cents=1000,
                requires_shipping=False,
                requires_accommodation_information=True,
                electronic_ticket=False,
                available=True,
                ordering=ordering(),
            ),
            dict(
                name='Lattiamajoitus 1 yö la-su - Pyynikin koulu (ei sis. makuualustaa)',
                description='Lattiamajoituspaikka lauantain ja sunnuntain väliseksi yöksi Pyynikin koululta. Pyynikin koulun majoituspaikat eivät sisällä makuualustaa, joten sinun tarvitsee tuoda makuupussi ja makuualusta tai patja.',
                limit_groups=[
                    limit_group('Majoitus Pyynikki la-su', 120),
                ],
                price_cents=1000,
                requires_shipping=False,
                requires_accommodation_information=True,
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

        if not meta.receipt_footer:
            meta.receipt_footer = u"Tracon ry / Yhdrek. nro. 194.820 / hallitus@tracon.fi"
            meta.save()


    def setup_payments(self):
        from payments.models import PaymentsEventMeta
        PaymentsEventMeta.get_or_create_dummy(event=self.event)


    def setup_programme(self):
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
            contact_email='Tracon -ohjelmatiimi <ohjelma@tracon.fi>',
        ))

        if settings.DEBUG:
            programme_event_meta.accepting_cold_offers_from = now() - timedelta(days=60)
            programme_event_meta.accepting_cold_offers_until = now() + timedelta(days=60)
            programme_event_meta.save()

        for room_name in [
            'Aaria',
            'Iso sali',
            'Pieni sali',
            # 'Sopraano', # Not in programme use
            'Rondo',
            'Studio',
            'Sonaatti 1',
            'Sonaatti 2',
            # 'Basso', # No longer exists
            # 'Opus 1', # No longer exists
            'Opus 2',
            'Opus 3',
            'Opus 4',
            'Talvipuutarha',
            'Puistolava',
            'Pieni ulkolava',
            'Puisto - Iso miittiteltta',
            'Puisto - Pieni miittiteltta',
            'Puisto - Bofferiteltta',
            'Muualla ulkona',
            'Duetto 2',
            'Riffi',
            'Maestro',
        ]:
            order = self.get_ordering_number() + 90000 # XXX

            room, created = Room.objects.get_or_create(
                venue=self.venue,
                name=room_name,
                defaults=dict(
                    order=order
                )
            )

            room.order = order
            room.save()

        for room_name in [
            'Sopraano',
            'Basso',
            'Opus 1',
        ]:
            room = Room.objects.get(venue=self.venue, name=room_name)
            room.active = False
            room.save()

        for pc_slug, role_title, role_is_default in [
            ('ohjelma', 'Ohjelmanjärjestäjä', True),
            ('ohjelma-2lk', 'Ohjelmanjärjestäjä (2. luokka)', False),
            ('ohjelma-3lk', 'Ohjelmanjärjestäjä (3. luokka)', False),
        ]:
            personnel_class = PersonnelClass.objects.get(event=self.event, slug=pc_slug)
            role, unused = Role.objects.get_or_create(
                personnel_class=personnel_class,
                title=role_title,
                defaults=dict(
                    is_default=role_is_default,
                )
            )

        have_categories = Category.objects.filter(event=self.event).exists()
        if not have_categories:
            for title, style in [
                ('Animeohjelma', 'anime'),
                ('Cosplayohjelma', 'cosplay'),
                ('Miitti', 'miitti'),
                ('Muu ohjelma', 'muu'),
                ('Roolipeliohjelma', 'rope'),
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
                category=Category.objects.get(title='Animeohjelma', event=self.event),
                title='Yaoi-paneeli',
                defaults=dict(
                    description='Kika-kika tirsk',
                )
            )

        for start_time, end_time in [
            (
                datetime(2016, 9, 3, 11, 0, 0, tzinfo=self.tz),
                datetime(2016, 9, 4, 1 , 0, 0, tzinfo=self.tz),
            ),
            (
                datetime(2016, 9, 4, 9 , 0, 0, tzinfo=self.tz),
                datetime(2016, 9, 4, 17, 0, 0, tzinfo=self.tz),
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
            start_time=datetime(2016, 9, 3, 10, 30, 0, tzinfo=self.tz),
        )

        # XXX
        # have_views = False
        have_views = View.objects.filter(event=self.event).exists()
        if not have_views:
            for view_name, room_names in [
                ('Pääohjelmatilat', [
                    'Iso sali',
                    'Pieni sali',
                    'Sonaatti 1',
                    'Sonaatti 2',
                    'Duetto 2',
                    'Maestro',
                ]),
            ]:
                rooms = [Room.objects.get(name__iexact=room_name, venue=self.venue)
                    for room_name in room_names]

                view, created = View.objects.get_or_create(event=self.event, name=view_name)
                view.rooms = rooms
                view.save()

    def setup_access(self):
        from access.models import Privilege, GroupPrivilege, EmailAliasType, GroupEmailAliasGrant

        # Grant accepted workers access to Tracon Slack
        privilege = Privilege.objects.get(slug='tracon-slack')
        for group in [
            self.event.labour_event_meta.get_group('accepted'),
            self.event.programme_event_meta.get_group('hosts'),
        ]:
            GroupPrivilege.objects.get_or_create(group=group, privilege=privilege, defaults=dict(event=self.event))

        cc_group = self.event.labour_event_meta.get_group('conitea')

        for metavar in [
            'etunimi.sukunimi',
            'nick',
        ]:
            alias_type = EmailAliasType.objects.get(domain__domain_name='tracon.fi', metavar=metavar)
            GroupEmailAliasGrant.objects.get_or_create(
                group=cc_group,
                type=alias_type,
                defaults=dict(
                    active_until=self.event.end_time,
                )
            )

    def setup_sms(self):
        from sms.models import SMSEventMeta

        sms_admin_group, = SMSEventMeta.get_or_create_groups(self.event, ['admins'])
        meta, unused = SMSEventMeta.objects.get_or_create(
            event=self.event,
            defaults=dict(
                admin_group=sms_admin_group,
                sms_enabled=True,
            )
        )


class Command(BaseCommand):
    args = ''
    help = 'Setup tracon10 specific stuff'

    def handle(self, *args, **opts):
        Setup().setup(test=settings.DEBUG)
