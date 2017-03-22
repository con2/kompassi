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
        self.setup_programme()

    def setup_core(self):
        from core.models import Venue, Event

        self.venue, unused = Venue.objects.get_or_create(name='Tampereen yliopisto', defaults=dict(
            name_inessive='Tampereen yliopistolla', # not really inessive though
        ))
        self.event, unused = Event.objects.get_or_create(slug='finncon2016', defaults=dict(
            name='Finncon 2016',
            name_genitive='Finncon 2016 -tapahtuman',
            name_illative='Finncon 2016 -tapahtumaan',
            name_inessive='Finncon 2016 -tapahtumassa',
            homepage_url='http://2016.finncon.org',
            organization_name='Finncon-yhdistys ry',
            organization_url='http://www.finncon.org',
            start_time=datetime(2016, 7, 1, 12, 0, tzinfo=self.tz),
            end_time=datetime(2016, 7, 3, 18, 0, tzinfo=self.tz),
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
        from ...models import SignupExtra, SpecialDiet
        from django.contrib.contenttypes.models import ContentType

        labour_admin_group, = LabourEventMeta.get_or_create_groups(self.event, ['admins'])

        if self.test:
            from core.models import Person
            person, unused = Person.get_or_create_dummy()
            labour_admin_group.user_set.add(person.user)

        content_type = ContentType.objects.get_for_model(SignupExtra)

        labour_event_meta_defaults = dict(
            signup_extra_content_type=content_type,
            work_begins=datetime(2016, 7, 1, 8, 0, tzinfo=self.tz),
            work_ends=datetime(2016, 7, 3, 20, 0, tzinfo=self.tz),
            admin_group=labour_admin_group,
            contact_email='Finncon 2016 -työvoimatiimi <tyovoima@finncon.org>',
        )

        if self.test:
            t = now()
            labour_event_meta_defaults.update(
                registration_opens=t - timedelta(days=60),
                registration_closes=t + timedelta(days=60),
            )
        else:
            # labour_event_meta_defaults.update(
            #     registration_opens=datetime(2015, 1, 22, 0, 0, tzinfo=self.tz),
            #     registration_closes=datetime(2015, 3, 14, 0, 0, tzinfo=self.tz),
            # )
            pass

        labour_event_meta, unused = LabourEventMeta.objects.get_or_create(
            event=self.event,
            defaults=labour_event_meta_defaults,
        )

        for pc_name, pc_slug, pc_app_label in [
            ('Conitea', 'conitea', 'labour'),
            ('Ylivänkäri', 'ylivankari', 'labour'),
            ('Työvoima', 'tyovoima', 'labour'),
            ('Ohjelmanjärjestäjä', 'ohjelma', 'programme'),
            ('Guest of Honour', 'goh', 'programme'),
            ('Media', 'media', 'badges'),
            ('Myyjä', 'myyja', 'badges'),
            ('Vieras', 'vieras', 'badges'),
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
        conitea = PersonnelClass.objects.get(event=self.event, slug='conitea')
        ylivankari = PersonnelClass.objects.get(event=self.event, slug='ylivankari')
        ohjelma = PersonnelClass.objects.get(event=self.event, slug='ohjelma')

        for name, description, pcs in [
            ('Conitea', 'Tapahtuman järjestelytoimikunnan eli Conitean jäsen', [conitea]),

            ('Info', 'Infopisteen henkilökunta vastaa kävijöiden kysymyksiin ja ratkaisee heidän ongelmiaan tapahtuman paikana. Tehtävä edellyttää asiakaspalveluasennetta, tervettä järkeä ja ongelmanratkaisukykyä.', [tyovoima, ylivankari]),
            ('Narikka', 'Narikassa ja isotavara- eli asenarikassa säilytetään tapahtuman aikana kävijöiden omaisuutta. Tehtävä ei vaadi erikoisosaamista.', [tyovoima, ylivankari]),
            ('Green room', 'Työvoiman ruokahuolto green roomissa. Edellyttää hygieniapassia.', [tyovoima, ylivankari]),
            ('Salivänkäri', 'Salivänkäri vastaa ohjelmasalien toiminnasta. He pitävät huolen, että ohjelmat alkavat ja loppuvat ajallaan ja että ohjelmanjärjestäjillä on kaikki mitä he tarvitsevat salissa.', [tyovoima, ylivankari]),
            ('Yleisvänkäri', 'Sekalaisia tehtäviä laidasta laitaan, jotka eivät vaadi erikoisosaamista. Voit halutessasi kirjata lisätietoihin, mitä osaat ja haluaisit tehdä.', [tyovoima, ylivankari]),
            ('Järjestyksenvalvoja', 'Kävijöiden turvallisuuden valvominen conipaikalla. Edellyttää voimassa olevaa JV-korttia ja asiakaspalveluasennetta. HUOM! Et voi valita tätä tehtävää hakemukseesi, ellet ole täyttänyt tietoihisi JV-kortin numeroa (oikealta ylhäältä oma nimesi > Pätevyydet).', [tyovoima, ylivankari]),
            ('Iltabileiden lipunmyyjä', 'Iltabileiden pääsylippujen myyntiä sekä tarkastamista. Myyjiltä edellytetään täysi-ikäisyyttä, asiakaspalveluhenkeä ja huolellisuutta rahankäsittelyssä. Vuoroja myös perjantaina.', [tyovoima, ylivankari]),
            ('Iltabileiden järjestyksenvalvoja', 'Kävijöiden turvallisuuden valvominen iltabileissä. Edellyttää voimassa olevaa JV-korttia ja asiakaspalveluasennetta. HUOM! Et voi valita tätä tehtävää hakemukseesi, ellet ole täyttänyt tietoihisi JV-kortin numeroa (oikealta ylhäältä oma nimesi > Pätevyydet).', [tyovoima, ylivankari]),
            ('Ensiapu', 'Toimit osana tapahtuman omaa ensiapuryhmää. Vuoroja päivisin ja öisin tapahtuman aukioloaikoina. Vaaditaan vähintään voimassa oleva EA1 -kortti ja osalta myös voimassa oleva EA2 -kortti. Kerro Työkokemus -kohdassa osaamisestasi, esim. oletko toiminut EA-tehtävissä tapahtumissa tai oletko sairaanhoitaja/lähihoitaja koulutuksestaltasi.', [tyovoima, ylivankari]),
            ('Erikoistehtävä', 'Mikäli olet sopinut erikseen työtehtävistä ja/tai sinut on ohjeistettu täyttämään lomake, valitse tämä ja kerro tarkemmin Vapaa alue -kentässä mihin tehtävään ja kenen toimesta sinut on valittu.', [tyovoima, ylivankari]),

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

        for slug in ['conitea']:
            JobCategory.objects.filter(event=self.event, slug=slug).update(public=False)

        for jc_name, qualification_name in [
            ('Järjestyksenvalvoja', 'JV-kortti'),
            ('Iltabileiden järjestyksenvalvoja', 'JV-kortti'),
        ]:
            jc = JobCategory.objects.get(event=self.event, name=jc_name)
            qual = Qualification.objects.get(name=qualification_name)

            jc.required_qualifications = [qual]
            jc.save()

        period_length = timedelta(hours=8)
        for period_description, period_start in [
            ('TODO', None),
            # (u"Perjantain kasaus (pe klo 14-18)", None),
            # (u"Lauantain aamuvuoro (la klo 08-11)", None),
            # (u"Lauantain päivävuoro (la klo 11-15)", None),
            # (u"Lauantain iltapäivävuoro (la klo 15-18)", None),
            # (u"Sunnuntain aamuvuoro (su klo 08-11)", None),
            # (u"Sunnuntain päivävuoro (su klo 11-15)", None),
            # (u"Sunnuntain purkuvuoro (su klo 15-17)", None),
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
            'Gluteeniton',
            'Laktoositon',
            'Maidoton',
            'Vegaaninen',
            'Lakto-ovo-vegetaristinen',
        ]:
            SpecialDiet.objects.get_or_create(name=diet_name)

        AlternativeSignupForm.objects.get_or_create(
            event=self.event,
            slug='conitea',
            defaults=dict(
                title='Conitean ilmoittautumislomake',
                signup_form_class_path='events.finncon2016.forms:OrganizerSignupForm',
                signup_extra_form_class_path='events.finncon2016.forms:OrganizerSignupExtraForm',
                active_from=datetime(2015, 8, 18, 0, 0, 0, tzinfo=self.tz),
                active_until=None,
            ),
        )

        for wiki_space, link_title, link_group in [
            ('FINNCONWORK', 'Työvoimawiki', 'accepted'),
        ]:
            InfoLink.objects.get_or_create(
                event=self.event,
                title=link_title,
                defaults=dict(
                    url='https://confluence.tracon.fi/display/{wiki_space}'.format(wiki_space=wiki_space),
                    group=labour_event_meta.get_group(link_group),
                )
            )

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
            contact_email='Finncon 2016 -ohjelmatiimi <ohjelma@2016.finncon.org>',
        ))

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
                ('Puheohjelma', 'anime'),
                ('Akateeminen ohjelma', 'cosplay'),
                ('Miitti', 'miitti'),
                ('Työpaja', 'rope'),
                ('Muu ohjelma', 'muu'),
            ]:
                Category.objects.get_or_create(
                    event=self.event,
                    style=style,
                    defaults=dict(
                        title=title,
                    )
                )

        for start_time, end_time in [
            (
                datetime(2016, 7, 1, 12, 0, 0, tzinfo=self.tz),
                datetime(2016, 7, 1, 18, 0, 0, tzinfo=self.tz),
            ),
            (
                datetime(2016, 7, 2, 10, 0, 0, tzinfo=self.tz),
                datetime(2016, 7, 2, 18, 0, 0, tzinfo=self.tz),
            ),
            (
                datetime(2016, 7, 3, 10, 0, 0, tzinfo=self.tz),
                datetime(2016, 7, 3, 18, 0, 0, tzinfo=self.tz),
            ),
        ]:
            TimeBlock.objects.get_or_create(
                event=self.event,
                start_time=start_time,
                defaults=dict(
                    end_time=end_time
                )
            )

        # SpecialStartTime.objects.get_or_create(
        #     event=self.event,
        #     start_time=datetime(2016, 9, 5, 10, 30, 0, tzinfo=self.tz),
        # )

        for view_name, room_names in [
            ('Pääohjelmatilat', [
                'Juhlasali',
                'Auditorio A1',
                'Luentosali A3',
                'Luentosali A4',
            ]),
            ('Toissijaiset ohjelmatilat', [
                'Auditorio D10a',
                'Auditorio D10b',
                'Auditorio D11',
                'Luentosali A05',
            ]),
        ]:
            rooms = [
                Room.objects.get_or_create(
                    venue=self.venue,
                    name=room_name,
                    defaults=dict(
                        order=self.get_ordering_number(),
                    )
                )[0]

                for room_name in room_names
            ]

            view, created = View.objects.get_or_create(event=self.event, name=view_name)
            if created:
                view.rooms = rooms
                view.save()


class Command(BaseCommand):
    args = ''
    help = 'Setup finncon2016 specific stuff'

    def handle(self, *args, **opts):
        Setup().setup(test=settings.DEBUG)
