# encoding: utf-8

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
        from core.models import Venue, Event

        self.venue, unused = Venue.objects.get_or_create(name='Tampere-talo')
        self.event, unused = Event.objects.get_or_create(slug='traconx', defaults=dict(
            name='Tracon X',
            name_genitive='Tracon X -tapahtuman',
            name_illative='Tracon X -tapahtumaan',
            name_inessive='Tracon X -tapahtumassa',
            homepage_url='http://2015.tracon.fi',
            organization_name='Tracon ry',
            organization_url='http://ry.tracon.fi',
            start_time=datetime(2015, 9, 5, 10, 0, tzinfo=self.tz),
            end_time=datetime(2015, 9, 6, 18, 0, tzinfo=self.tz),
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
            person, unused = Person.get_or_create_dummy()
            labour_admin_group.user_set.add(person.user)

        content_type = ContentType.objects.get_for_model(SignupExtra)

        labour_event_meta_defaults = dict(
            signup_extra_content_type=content_type,
            work_begins=datetime(2015, 9, 4, 8, 0, tzinfo=self.tz),
            work_ends=datetime(2015, 9, 6, 22, 0, tzinfo=self.tz),
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
            labour_event_meta_defaults.update(
                registration_opens=datetime(2015, 3, 19, 18, 0, tzinfo=self.tz),
                registration_closes=datetime(2015, 8, 1, 0, 0, tzinfo=self.tz),
            )
            pass

        labour_event_meta, unused = LabourEventMeta.objects.get_or_create(
            event=self.event,
            defaults=labour_event_meta_defaults,
        )

        self.afterparty_perk, unused = Perk.objects.get_or_create(
            event=self.event,
            slug='kaatajaiset',
            defaults=dict(
                name=u'Kaatajaiset',
            ),
        )

        fmh = PersonnelClass.objects.filter(event=self.event, slug='ylivankari')
        if fmh.exists():
            fmh.update(name=u'Vuorovastaava', slug='vuorovastaava')

        for pc_name, pc_slug, pc_app_label, pc_afterparty in [
            (u'Conitea', 'conitea', 'labour', True),
            (u'Vuorovastaava', 'vuorovastaava', 'labour', True),
            (u'Työvoima', 'tyovoima', 'labour', True),
            (u'Ohjelmanjärjestäjä', 'ohjelma', 'programme', True),
            (u'Guest of Honour', 'goh', 'programme', False), # tervetullut muttei kutsuta automaattiviestillä
            (u'Media', 'media', 'badges', False),
            (u'Myyjä', 'myyja', 'badges', False),
            (u'Vieras', 'vieras', 'badges', False),
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

        for name, description, pcs in [
            (u'Conitea', u'Tapahtuman järjestelytoimikunnan eli conitean jäsen', [conitea]),

            (u'Erikoistehtävä', u'Mikäli olet sopinut erikseen työtehtävistä ja/tai sinut on ohjeistettu täyttämään lomake, valitse tämä ja kerro tarkemmin Vapaa alue -kentässä mihin tehtävään ja kenen toimesta sinut on valittu.', [tyovoima, vuorovastaava]),
            (u'Järjestyksenvalvoja', u'Kävijöiden turvallisuuden valvominen conipaikalla ja yömajoituksessa. Edellyttää voimassa olevaa JV-korttia ja asiakaspalveluasennetta. HUOM! Et voi valita tätä tehtävää hakemukseesi, ellet ole täyttänyt tietoihisi JV-kortin numeroa (oikealta ylhäältä oma nimesi &gt; Pätevyydet).', [tyovoima, vuorovastaava]),
            (u'Kasaus ja purku', u'Kalusteiden siirtelyä & opasteiden kiinnittämistä. Ei vaadi erikoisosaamista. Työvuoroja myös jo pe sekä su conin sulkeuduttua, kerro lisätiedoissa jos voit osallistua näihin.', [tyovoima, vuorovastaava]),
            (u'Logistiikka', u'Autokuskina toimimista ja tavaroiden/ihmisten hakua ja noutamista. B-luokan ajokortti vaaditaan. Työvuoroja myös perjantaille.', [tyovoima, vuorovastaava]),
            (u'Majoitusvalvoja', u'Huolehtivat lattiamajoituspaikkojen pyörittämisestä yöaikaan. Työvuoroja myös molempina öinä.', [tyovoima, vuorovastaava]),
            (u'Myynti', u'Pääsylippujen ja Tracon-oheistuotteiden myyntiä sekä lippujen tarkastamista. Myyjiltä edellytetään täysi-ikäisyyttä, asiakaspalveluhenkeä ja huolellisuutta rahankäsittelyssä. Vuoroja myös perjantaina.', [tyovoima, vuorovastaava]),
            (u'Narikka', u'Narikassa ja isotavara- eli asenarikassa säilytetään tapahtuman aikana kävijöiden omaisuutta. Tehtävä ei vaadi erikoisosaamista.', [tyovoima, vuorovastaava]),
            (u'Ohjelma-avustaja', u'Lautapelien pyörittämistä, karaoken valvontaa, cosplay-kisaajien avustamista. Kerro Vapaa alue -kohdassa tarkemmin, mitä haluaisit tehdä. Huom! Puheohjelmasalien vänkäreiltä toivotaan AV-tekniikan osaamista.', [tyovoima, vuorovastaava]),
            (u'Green room', u'Työvoiman ruokahuolto green roomissa. Edellyttää hygieniapassia.', [tyovoima, vuorovastaava]),
            (u'Taltiointi', u'Taltioinnin keskeisiin tehtäviin kuuluvat mm. saleissa esitettävien ohjelmanumeroiden videointi tapahtumassa ja editointi tapahtuman jälkeen. Lisäksi videoidaan dokumentaarisella otteella myös yleisesti tapahtumaa. Kerro Työkokemus-kentässä aiemmasta videokuvauskokemuksestasi (esim. linkkejä videogallerioihisi) sekä mitä haluaisit taltioinnissa tehdä.', [tyovoima, vuorovastaava]),
            (u'Tekniikka', u'Salitekniikan (AV) ja tietotekniikan (tulostimet, lähiverkot, WLAN) nopeaa MacGyver-henkistä ongelmanratkaisua.', [tyovoima, vuorovastaava]),
            (u'Valokuvaus', u'Valokuvaus tapahtuu pääasiassa kuvaajien omilla järjestelmäkameroilla. Tehtäviä voivat olla studiokuvaus, salikuvaus sekä yleinen valokuvaus. Kerro Työkokemus-kentässä aiemmasta valokuvauskokemuksestasi (esim. linkkejä kuvagallerioihisi) sekä mitä/missä haluaisit tapahtumassa valokuvata.', [tyovoima, vuorovastaava]),
            (u'Yleisvänkäri', u'Sekalaisia tehtäviä laidasta laitaan, jotka eivät vaadi erikoisosaamista. Voit halutessasi kirjata lisätietoihin, mitä osaat ja haluaisit tehdä.', [tyovoima, vuorovastaava]),
            (u'Info', u'Infopisteen henkilökunta vastaa kävijöiden kysymyksiin ja ratkaisee heidän ongelmiaan tapahtuman paikana. Tehtävä edellyttää asiakaspalveluasennetta, tervettä järkeä ja ongelmanratkaisukykyä.', [tyovoima, vuorovastaava]),

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
            (u'Logistiikka', u'Henkilöauton ajokortti (B)'),
            (u'Green room', u'Hygieniapassi'),
        ]:
            jc = JobCategory.objects.get(event=self.event, name=jc_name)
            qual = Qualification.objects.get(name=qualification_name)
            if not jc.required_qualifications.exists():
                jc.required_qualifications = [qual]
                jc.save()

        event_starts = datetime(2015, 9, 5, 10, 0, tzinfo=self.tz)
        event_ends = datetime(2015, 9, 6, 18, 0, tzinfo=self.tz)
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
            u'Gluteeniton',
            u'Laktoositon',
            u'Maidoton',
            u'Vegaaninen',
            u'Lakto-ovo-vegetaristinen',
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
                signup_form_class_path='events.traconx.forms:OrganizerSignupForm',
                signup_extra_form_class_path='events.traconx.forms:OrganizerSignupExtraForm',
                active_from=datetime(2014, 11, 15, 12, 0, 0, tzinfo=self.tz),
                active_until=datetime(2015, 11, 22, 23, 59, 59, tzinfo=self.tz),
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
            reference_number_template="2015{:05d}",
            contact_email='Traconin lipunmyynti <liput@tracon.fi>',
            plain_contact_email='liput@tracon.fi',
            ticket_free_text=u"Tämä on sähköinen lippusi Tracon X -tapahtumaan. Sähköinen lippu vaihdetaan rannekkeeseen\n"
                u"lipunvaihtopisteessä saapuessasi tapahtumaan. Voit tulostaa tämän lipun tai näyttää sen\n"
                u"älypuhelimen tai tablettitietokoneen näytöltä. Mikäli kumpikaan näistä ei ole mahdollista, ota ylös\n"
                u"kunkin viivakoodin alla oleva neljästä tai viidestä sanasta koostuva sanakoodi ja ilmoita se\n"
                u"lipunvaihtopisteessä.\n\n"
                u"Tervetuloa Traconiin!",
            front_page_text=u"<h2>Tervetuloa ostamaan pääsylippuja Tracon X -tapahtumaan!</h2>"
                u"<p>Liput maksetaan suomalaisilla verkkopankkitunnuksilla heti tilauksen yhteydessä.</p>"
                u"<p>Lue lisää tapahtumasta <a href='http://2015.tracon.fi'>Traconin kotisivuilta</a>.</p>",
        )

        if self.test:
            t = now()
            defaults.update(
                ticket_sales_starts=t - timedelta(days=60),
                ticket_sales_ends=t + timedelta(days=60),
            )
        else:
            defaults.update(
                ticket_sales_starts=datetime(2014, 12, 1, 0, 0, tzinfo=self.tz),
                ticket_sales_ends=datetime(2015, 12, 12, 23, 59, 59, tzinfo=self.tz),
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
                name=u'Joulupaketti - 2 kpl viikonloppulippu ja 1 kpl kalenteri',
                description=u'Paketti sisältää kaksi viikonloppulippua ja yhden Tracon 2015 -seinäkalenterin. Tuotteet toimitetaan antamaasi osoitteeseen postitse, ja postikulut sisältyvät hintaan.',
                internal_description=u'HUOM! Järjestelmä ei tue lippukiintiöiden kuluttamista kahdella per myyty paketti, joten lippukiintiöt täytyy korjata käsin kun joulupaketit on myyty.',
                limit_groups=[
                    # limit_group('Lauantain liput', 5000, 2),
                    # limit_group('Sunnuntain liput', 5000, 2),
                    limit_group('Joulupaketti A', 80),
                ],
                price_cents=6000,
                requires_shipping=True,
                electronic_ticket=False,
                available=False,
                ordering=ordering(),
            ),
            dict(
                name=u'Joulupaketti - 1 kpl viikonloppulippu ja 1 kpl kalenteri',
                description=u'Paketti sisältää yhden viikonloppulipun ja yhden Tracon 2015 -seinäkalenterin. Tuotteet toimitetaan antamaasi osoitteeseen postitse, ja postikulut sisältyvät hintaan.',
                limit_groups=[
                    limit_group('Lauantain liput', 3525),
                    limit_group('Sunnuntain liput', 3525),
                    limit_group('Joulupaketti B', 80),
                ],
                price_cents=3500,
                requires_shipping=True,
                electronic_ticket=False,
                available=False,
                ordering=ordering(),
            ),
            dict(
                name=u'Viikonloppulippu',
                description=u'Viikonloppulippu Tracon 2015 -tapahtumaan. Voimassa koko viikonlopun ajan la klo 10 – su klo 18. Toimitetaan sähköpostitse PDF-tiedostona, jossa olevaa viivakoodia vastaan saat rannekkeen tapahtumaan saapuessasi.',
                limit_groups=[
                    limit_group('Lauantain liput', 3525),
                    limit_group('Sunnuntain liput', 3525),
                ],
                price_cents=2500,
                requires_shipping=False,
                electronic_ticket=True,
                available=True,
                ordering=ordering(),
            ),
            dict(
                name=u'Lauantailippu',
                description=u'Lauantailippu Tracon 2015 -tapahtumaan. Voimassa koko lauantaipäivän ajan la klo 10 – su klo 08. Toimitetaan sähköpostitse PDF-tiedostona, jossa olevaa viivakoodia vastaan saat rannekkeen tapahtumaan saapuessasi.',
                limit_groups=[
                    limit_group('Lauantain liput', 3525),
                ],
                price_cents=1800,
                requires_shipping=False,
                electronic_ticket=True,
                available=True,
                ordering=ordering(),
            ),
            dict(
                name=u'Sunnuntailippu',
                description=u'Lauantailippu Tracon 2015 -tapahtumaan. Voimassa koko sunnuntaipäivän ajan su klo 00 - su klo 18. Toimitetaan sähköpostitse PDF-tiedostona, jossa olevaa viivakoodia vastaan saat rannekkeen tapahtumaan saapuessasi.',
                limit_groups=[
                    limit_group('Sunnuntain liput', 3525),
                ],
                price_cents=1500,
                requires_shipping=False,
                electronic_ticket=True,
                available=True,
                ordering=ordering(),
            ),
            dict(
                name=u'Konserttipaketti Traconin kävijälle',
                description=u'Sisältää liput The Super Sound of Videogames 2 -konserttiin sekä Traconin iltabileisiin.</p><p>'
                    u'The Super Sound of Videogames 2 -konsertti perjantaina 4. syyskuuta klo 19 Tampere-talossa. Esiintymässä QUINSONITUS ja TAKOMO PERCUSSION. Lisätietoja <a href="http://www.tampere-talo.fi/supersound" target="_blank">Tampere-talon sivuilta</a> (avautuu uuteen ikkunaan).</p><p>'
                    u'Traconin iltabileet Pakkahuoneella lauantaina 5. syyskuuta 2015 kello 19–01. Esiintymässä MACHINAE SUPREMACY (SWE) sekä YOHIO (SWE) + DJ:t Klubilla. Ei sisällä narikkamaksua 2 €.</p><p>'
                    u'HUOM! Tämä lippu oikeuttaa pääsyyn tilaisuuksiin vain yhdessä Tracon-rannekkeen kanssa (lauantai, sunnuntai tai koko viikonloppu).',
                limit_groups=[
                    limit_group('Iltabileliput', 1200),
                    limit_group('The Super Sound of Videogames 2', 500),
                ],
                price_cents=3000,
                requires_shipping=False,
                electronic_ticket=True,
                available=True,
                ordering=ordering(),
            ),
            dict(
                name=u'Iltabilelippu Traconin kävijälle',
                description=u'Traconin iltabileet Pakkahuoneella lauantaina 5. syyskuuta 2015 kello 19–01. Esiintymässä MACHINAE SUPREMACY (SWE) sekä YOHIO (SWE) + DJ:t Klubilla. Ei sisällä narikkamaksua 2 €.</p><p>'
                    u'HUOM! Tämä lippu oikeuttaa pääsyyn Traconin iltabileisiin vain yhdessä Tracon-rannekkeen kanssa (lauantai, sunnuntai tai koko viikonloppu).',
                limit_groups=[
                    limit_group('Iltabileliput', 1200),
                ],
                price_cents=1000,
                requires_shipping=False,
                electronic_ticket=True,
                available=True,
                ordering=ordering(),
            ),
            dict(
                name=u'Iltabilelippu ei-kävijälle',
                description=u'Traconin iltabileet Pakkahuoneella lauantaina 5. syyskuuta 2015 kello 19–01. Esiintymässä MACHINAE SUPREMACY (SWE) sekä YOHIO (SWE) + DJ:t Klubilla. Ei sisällä narikkamaksua 2 €.</p><p>'
                    u'Tämä lippu oikeuttaa pääsyyn Traconin iltabileisiin ilman Tracon-ranneketta.',
                limit_groups=[
                    limit_group('Iltabileliput', 1200),
                ],
                price_cents=2000,
                requires_shipping=False,
                electronic_ticket=True,
                available=True,
                ordering=ordering(),
            ),
            dict(
                name=u'Lattiamajoitus 1 yö pe-la - Aleksanterin koulu (sis. makuualusta)',
                description=u'Lattiamajoituspaikka perjantain ja lauantain väliseksi yöksi Aleksanterin koululta. Aleksanterin koulun majoituspaikat sisältävät makuualustan, joten sinun tarvitsee tuoda vain makuupussi.',
                limit_groups=[
                    limit_group('Majoitus Aleksanteri pe-la', 80),
                ],
                price_cents=1300,
                requires_shipping=False,
                requires_accommodation_information=True,
                electronic_ticket=False,
                available=self.test,
                ordering=ordering(),
            ),
            dict(
                name=u'Lattiamajoitus 1 yö la-su - Aleksanterin koulu (sis. makuualusta)',
                description=u'Lattiamajoituspaikka lauantain ja sunnuntain väliseksi yöksi Aleksanterin koululta. Aleksanterin koulun majoituspaikat sisältävät makuualustan, joten sinun tarvitsee tuoda vain makuupussi.',
                limit_groups=[
                    limit_group('Majoitus Aleksanteri la-su', 130),
                ],
                price_cents=1300,
                requires_shipping=False,
                requires_accommodation_information=True,
                electronic_ticket=False,
                available=self.test,
                ordering=ordering(),
            ),
            dict(
                name=u'Lattiamajoitus 1 yö pe-la - Pyynikin koulu (ei sis. makuualustaa)',
                description=u'Lattiamajoituspaikka perjantain ja lauantain väliseksi yöksi Pyynikin koululta. Pyynikin koulun majoituspaikat eivät sisällä makuualustaa, joten sinun tarvitsee tuoda makuupussi ja makuualusta tai patja.',
                limit_groups=[
                    limit_group('Majoitus Pyynikki pe-la', 120),
                ],
                price_cents=1000,
                requires_shipping=False,
                requires_accommodation_information=True,
                electronic_ticket=False,
                available=self.test,
                ordering=ordering(),
            ),
            dict(
                name=u'Lattiamajoitus 1 yö la-su - Pyynikin koulu (ei sis. makuualustaa)',
                description=u'Lattiamajoituspaikka lauantain ja sunnuntain väliseksi yöksi Pyynikin koululta. Pyynikin koulun majoituspaikat eivät sisällä makuualustaa, joten sinun tarvitsee tuoda makuupussi ja makuualusta tai patja.',
                limit_groups=[
                    limit_group('Majoitus Pyynikki la-su', 120),
                ],
                price_cents=1000,
                requires_shipping=False,
                requires_accommodation_information=True,
                electronic_ticket=False,
                available=self.test,
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

        programme_admin_group, = ProgrammeEventMeta.get_or_create_groups(self.event, ['admins'])
        programme_event_meta, unused = ProgrammeEventMeta.objects.get_or_create(event=self.event, defaults=dict(
            public=False,
            admin_group=programme_admin_group,
            contact_email='Tracon X -ohjelmatiimi <ohjelma@tracon.fi>',
        ))

        for room_name in [
            u'Aaria',
            u'Iso sali',
            u'Pieni sali',
            # u'Sopraano', # Ei luento-ohjelmakäytössä
            u'Rondo',
            u'Studio',
            u'Sonaatti 1',
            u'Sonaatti 2',
            u'Basso',
            #u'Opus 1', # No longer in use
            u'Opus 2',
            u'Opus 3',
            u'Opus 4',
            u'Talvipuutarha',
            u'Puistolava',
            u'Pieni ulkolava',
            u'Puisto - Iso miittiteltta',
            u'Puisto - Pieni miittiteltta',
            u'Puisto - Bofferiteltta',
            u'Muualla ulkona',
        ]:
            order = self.get_ordering_number() + 80000 # XXX

            room, created = Room.objects.get_or_create(
                venue=self.venue,
                name=room_name,
                defaults=dict(
                    order=order
                )
            )

            room.order = order
            room.save()

        personnel_class = PersonnelClass.objects.get(event=self.event, slug='ohjelma')
        role, unused = Role.objects.get_or_create(
            personnel_class=personnel_class,
            title=u'Ohjelmanjärjestäjä',
            defaults=dict(
                is_default=True,
                require_contact_info=True,
            )
        )

        have_categories = Category.objects.filter(event=self.event).exists()
        if not have_categories:
            for title, style in [
                (u'Animeohjelma', u'anime'),
                (u'Cosplayohjelma', u'cosplay'),
                (u'Miitti', u'miitti'),
                (u'Muu ohjelma', u'muu'),
                (u'Roolipeliohjelma', u'rope'),
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
                datetime(2015, 9, 5, 11, 0, 0, tzinfo=self.tz),
                datetime(2015, 9, 6, 1 , 0, 0, tzinfo=self.tz),
            ),
            (
                datetime(2015, 9, 6, 9 , 0, 0, tzinfo=self.tz),
                datetime(2015, 9, 6, 17, 0, 0, tzinfo=self.tz),
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
            start_time=datetime(2015, 9, 5, 10, 30, 0, tzinfo=self.tz),
        )

        have_views = View.objects.filter(event=self.event).exists()
        if not have_views:
            for view_name, room_names in [
                (u'Pääohjelmatilat', [
                    u'Iso sali',
                    u'Pieni sali',
                    u'Studio',
                    u'Sonaatti 1',
                    u'Sonaatti 2',
                ]),
                (u'Toissijaiset ohjelmatilat', [
                    u'Aaria',
                    u'Rondo',
                    u'Opus 2',
                    u'Opus 3',
                    u'Opus 4',
                    u'Talvipuutarha',
                ]),
                (u'Ulko-ohjelma', [
                    u'Puistolava',
                    u'Puisto - Iso miittiteltta',
                    u'Puisto - Pieni miittiteltta',
                    u'Muualla ulkona',
                ]),
            ]:
                rooms = [Room.objects.get(name__iexact=room_name, venue=self.venue)
                    for room_name in room_names]

                view, created = View.objects.get_or_create(event=self.event, name=view_name)
                view.rooms = rooms
                view.save()

    def setup_access(self):
        from access.models import Privilege, GroupPrivilege

        # Grant accepted workers access to Tracon Slack
        group = self.event.labour_event_meta.get_group('accepted')
        privilege = Privilege.objects.get(slug='tracon-slack')
        GroupPrivilege.objects.get_or_create(group=group, privilege=privilege, defaults=dict(event=self.event))

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
