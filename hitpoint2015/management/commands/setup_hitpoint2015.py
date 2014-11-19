# encoding: utf-8

from datetime import datetime, timedelta

from django.core.management.base import BaseCommand, make_option
from django.utils.timezone import get_default_timezone, now

from core.utils import slugify


class Setup(object):
    def __init__(self):
        self._ordering = 0

    def get_ordering_number(self):
        self._ordering += 10
        return self._ordering

    def setup(self, test=False):
        self.test = test
        self.tz = get_default_timezone()
        self.setup_core()
        self.setup_labour()

    def setup_core(self):
        from core.models import Venue, Event

        self.venue, unused = Venue.objects.get_or_create(
            name='Ilmoitetaan myöhemmin',
            name_inessive='Ilmoitetaan myöhemmin',
        )
        self.event, unused = Event.objects.get_or_create(slug='hitpoint2015', defaults=dict(
            name='Tracon Hitpoint 2015',
            name_genitive='Tracon Hitpoint 2015 -tapahtuman',
            name_illative='Tracon Hitpoint 2015 -tapahtumaan',
            name_inessive='Tracon Hitpoint 2015 -tapahtumassa',
            homepage_url='http://2015.hitpoint.tracon.fi',
            organization_name='Tracon ry',
            organization_url='http://ry.tracon.fi',
            start_time=None, # datetime(2015, 11, 21, 10, 0, tzinfo=self.tz),
            end_time=None, # datetime(2015, 11, 22, 18, 0, tzinfo=self.tz),
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

        labour_admin_group, created = LabourEventMeta.get_or_create_group(self.event, 'admins')

        if self.test and created:
            person, unused = Person.get_or_create_dummy()
            labour_admin_group.user_set.add(person.user)

        content_type = ContentType.objects.get_for_model(SignupExtra)

        labour_event_meta_defaults = dict(
            signup_extra_content_type=content_type,
            work_begins=datetime(2015, 9, 4, 8, 0, tzinfo=self.tz),
            work_ends=datetime(2015, 9, 6, 22, 0, tzinfo=self.tz),
            admin_group=labour_admin_group,
            contact_email='Tracon Hitpoint 2015 -työvoimatiimi <hitpoint@tracon.fi>',
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

        self.afterparty_perk, unused = Perk.objects.get_or_create(
            event=self.event,
            slug='kaatajaiset',
            defaults=dict(
                name=u'Kaatajaiset',
            ),
        )

        for pc_name, pc_slug, pc_app_label, pc_afterparty in [
            (u'Conitea', 'conitea', 'labour', True),
            (u'Ylivänkäri', 'ylivankari', 'labour', True),
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
        ylivankari = PersonnelClass.objects.get(event=self.event, slug='ylivankari')
        ohjelma = PersonnelClass.objects.get(event=self.event, slug='ohjelma')

        for name, description, pcs in [
            (u'Conitea', u'Tapahtuman järjestelytoimikunnan eli conitean jäsen', [conitea]),

            (u'Erikoistehtävä', u'Mikäli olet sopinut erikseen työtehtävistä ja/tai sinut on ohjeistettu täyttämään lomake, valitse tämä ja kerro tarkemmin Vapaa alue -kentässä mihin tehtävään ja kenen toimesta sinut on valittu.', [tyovoima, ylivankari]),
            (u'Järjestyksenvalvoja', u'Kävijöiden turvallisuuden valvominen conipaikalla ja yömajoituksessa. Edellyttää voimassa olevaa JV-korttia ja asiakaspalveluasennetta. HUOM! Et voi valita tätä tehtävää hakemukseesi, ellet ole täyttänyt tietoihisi JV-kortin numeroa (oikealta ylhäältä oma nimesi &gt; Pätevyydet).', [tyovoima, ylivankari]),
            (u'Ensiapu', 'Toimit osana tapahtuman omaa ensiapuryhmää. Vuoroja päivisin ja öisin tapahtuman aukioloaikoina. Vaaditaan vähintään voimassa oleva EA1 -kortti ja osalta myös voimassa oleva EA2 -kortti. Kerro Työkokemus -kohdassa osaamisestasi, esim. oletko toiminut EA-tehtävissä tapahtumissa tai oletko sairaanhoitaja/lähihoitaja koulutuksestaltasi.', [tyovoima, ylivankari]),
            (u'Kasaus ja purku', u'Kalusteiden siirtelyä & opasteiden kiinnittämistä. Ei vaadi erikoisosaamista. Työvuoroja myös jo pe sekä su conin sulkeuduttua, kerro lisätiedoissa jos voit osallistua näihin.', [tyovoima, ylivankari]),
            (u'Logistiikka', u'Autokuskina toimimista ja tavaroiden/ihmisten hakua ja noutamista. B-luokan ajokortti vaaditaan. Työvuoroja myös perjantaille.', [tyovoima, ylivankari]),
            (u'Majoitusvalvoja', u'Huolehtivat lattiamajoituspaikkojen pyörittämisestä yöaikaan. Työvuoroja myös molempina öinä.', [tyovoima, ylivankari]),
            (u'Myynti', u'Pääsylippujen ja Tracon-oheistuotteiden myyntiä sekä lippujen tarkastamista. Myyjiltä edellytetään täysi-ikäisyyttä, asiakaspalveluhenkeä ja huolellisuutta rahankäsittelyssä. Vuoroja myös perjantaina.', [tyovoima, ylivankari]),
            (u'Narikka', u'Narikassa ja isotavara- eli asenarikassa säilytetään tapahtuman aikana kävijöiden omaisuutta. Tehtävä ei vaadi erikoisosaamista.', [tyovoima, ylivankari]),
            (u'Ohjelma-avustaja', u'Lautapelien pyörittämistä, karaoken valvontaa, cosplay-kisaajien avustamista. Kerro Vapaa alue -kohdassa tarkemmin, mitä haluaisit tehdä. Huom! Puheohjelmasalien vänkäreiltä toivotaan AV-tekniikan osaamista.', [tyovoima, ylivankari]),
            (u'Green room', u'Työvoiman ruokahuolto green roomissa. Hygieniapassi suositeltava.', [tyovoima, ylivankari]),
            (u'Taltiointi', u'Taltioinnin keskeisiin tehtäviin kuuluvat mm. saleissa esitettävien ohjelmanumeroiden videointi tapahtumassa ja editointi tapahtuman jälkeen. Lisäksi videoidaan dokumentaarisella otteella myös yleisesti tapahtumaa. Kerro Työkokemus-kentässä aiemmasta videokuvauskokemuksestasi (esim. linkkejä videogallerioihisi) sekä mitä haluaisit taltioinnissa tehdä.', [tyovoima, ylivankari]),
            (u'Tekniikka', u'Salitekniikan (AV) ja tietotekniikan (tulostimet, lähiverkot, WLAN) nopeaa MacGyver-henkistä ongelmanratkaisua.', [tyovoima, ylivankari]),
            (u'Valokuvaus', u'Valokuvaus tapahtuu pääasiassa kuvaajien omilla järjestelmäkameroilla. Tehtäviä voivat olla studiokuvaus, salikuvaus sekä yleinen valokuvaus. Kerro Työkokemus-kentässä aiemmasta valokuvauskokemuksestasi (esim. linkkejä kuvagallerioihisi) sekä mitä/missä haluaisit tapahtumassa valokuvata.', [tyovoima, ylivankari]),
            (u'Yleisvänkäri', u'Sekalaisia tehtäviä laidasta laitaan, jotka eivät vaadi erikoisosaamista. Voit halutessasi kirjata lisätietoihin, mitä osaat ja haluaisit tehdä.', [tyovoima, ylivankari]),
            (u'Info', u'Infopisteen henkilökunta vastaa kävijöiden kysymyksiin ja ratkaisee heidän ongelmiaan tapahtuman paikana. Tehtävä edellyttää asiakaspalveluasennetta, tervettä järkeä ja ongelmanratkaisukykyä.', [tyovoima, ylivankari]),

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

        period_length = timedelta(hours=8)
        for period_description, period_start in [
            ("Lauantain aamuvuoro (la klo 08-16)", None),
            ("Lauantain iltavuoro (la klo 16-24)", None),
            ("Lauantai-sunnuntai-yövuoro (su klo 00-08)", None),
            ("Sunnuntain aamuvuoro (su klo 08-16)", None),
            ("Sunnuntain iltavuoro (su klo 16-20)", None),
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
                signup_form_class_path='hitpoint2015.forms:OrganizerSignupForm',
                signup_extra_form_class_path='hitpoint2015.forms:OrganizerSignupExtraForm',
                active_from=datetime(2014, 11, 15, 12, 0, 0, tzinfo=self.tz),
                active_until=datetime(2015, 11, 22, 23, 59, 59, tzinfo=self.tz),
            ),
        )

        for wiki_space, link_title, link_group in [
            ('HITPTWORK', 'Työvoimawiki', 'accepted'),
            ('HITPTINFO', 'Infowiki', 'info'),
        ]:
            InfoLink.objects.get_or_create(
                event=self.event,
                title=link_title,
                defaults=dict(
                    url='https://confluence.tracon.fi/display/{wiki_space}'.format(wiki_space=wiki_space),
                    group=labour_event_meta.get_group(link_group),
                )
            )


class Command(BaseCommand):
    args = ''
    help = 'Setup hitpoint2015 specific stuff'

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
