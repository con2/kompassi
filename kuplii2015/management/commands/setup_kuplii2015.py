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

        self.venue, unused = Venue.objects.get_or_create(name='Finlaysonin alue', defaults=dict(
            name_inessive='Finlaysonin alueella', # not really inessive though
        ))
        self.event, unused = Event.objects.get_or_create(slug='kuplii2015', defaults=dict(
            name='Tampere Kuplii 2015',
            name_genitive='Tampere Kuplii 2015 -tapahtuman',
            name_illative='Tampere Kuplii 2015 -tapahtumaan',
            name_inessive='Tampere Kuplii 2015 -tapahtumassa',
            homepage_url='http://2015.tamperekuplii.fi',
            organization_name='Tampere Kuplii ry ry',
            organization_url='http://ry.tamperekuplii.fi',
            start_time=datetime(2015, 3, 28, 10, 0, tzinfo=self.tz),
            end_time=datetime(2015, 3, 29, 17, 0, tzinfo=self.tz),
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

        labour_admin_group, created = LabourEventMeta.get_or_create_group(self.event, 'admins')

        if self.test and created:
            from core.models import Person
            person, unused = Person.get_or_create_dummy()
            labour_admin_group.user_set.add(person.user)

        content_type = ContentType.objects.get_for_model(SignupExtra)

        labour_event_meta_defaults = dict(
            signup_extra_content_type=content_type,
            work_begins=datetime(2015, 3, 27, 14, 0, tzinfo=self.tz),
            work_ends=datetime(2015, 3,29, 18, 0, tzinfo=self.tz),
            admin_group=labour_admin_group,
            contact_email='Tampere Kupliin työvoimatiimi <tyovoima@tamperekuplii.fi>',
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
            (u'Kuplitea', 'kuplitea', 'labour', True),
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
        kuplitea = PersonnelClass.objects.get(event=self.event, slug='kuplitea')
        ylivankari = PersonnelClass.objects.get(event=self.event, slug='ylivankari')
        ohjelma = PersonnelClass.objects.get(event=self.event, slug='ohjelma')

        for name, description, pcs in [
            (u'Kuplitea', u'Tapahtuman järjestelytoimikunnan eli kuplitean jäsen', [kuplitea]),

            (u'Erikoistehtävä', u'Mikäli olet sopinut erikseen työtehtävistä ja/tai sinut on ohjeistettu täyttämään lomake, valitse tämä ja kerro tarkemmin Vapaa alue -kentässä mihin tehtävään ja kenen toimesta sinut on valittu.', [tyovoima, ylivankari]),
            (u'Järjestyksenvalvoja', u'Kävijöiden turvallisuuden valvominen conipaikalla. Edellyttää voimassa olevaa JV-korttia ja asiakaspalveluasennetta. HUOM! Et voi valita tätä tehtävää hakemukseesi, ellet ole täyttänyt tietoihisi JV-kortin numeroa (oikealta ylhäältä oma nimesi > Pätevyydet).', [tyovoima, ylivankari]),
            (u'Kasaus ja purku', u'Kalusteiden siirtelyä & opasteiden kiinnittämistä. Ei vaadi erikoisosaamista. Työvuoroja myös jo pe kello 14-18 sekä su kello 19 asti, kerro lisätiedoissa jos voit osallistua näihin.', [tyovoima, ylivankari]),
            (u'Yleisvänkäri', u'Sekalaisia tehtäviä laidasta laitaan, jotka eivät vaadi erikoisosaamista. Voit halutessasi kirjata lisätietoihin, mitä osaat ja haluaisit tehdä.', [tyovoima, ylivankari]),
            (u'Info', u'Infopisteen henkilökunta vastaa kävijöiden kysymyksiin ja ratkaisee heidän ongelmiaan tapahtuman paikana. Tehtävä edellyttää asiakaspalveluasennetta, tervettä järkeä ja ongelmanratkaisukykyä.', [tyovoima, ylivankari]),
            (u'Salivänkäri', u'Salivänkäri vastaa ohjelmasalien toiminnasta. He pitävät huolen, että ohjelmat alkavat ja loppuvat ajallaan ja että ohjelmanjärjestäjillä on kaikki mitä he tarvitsevat salissa.', [tyovoima, ylivankari]),

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

        for name in [u'Kuplitea']:
            JobCategory.objects.filter(event=self.event, name=name).update(public=False)

        for jc_name, qualification_name in [
            (u'Järjestyksenvalvoja', u'JV-kortti'),
        ]:
            jc = JobCategory.objects.get(event=self.event, name=jc_name)
            qual = Qualification.objects.get(name=qualification_name)

        period_length = timedelta(hours=8)
        for period_description, period_start in [
            (u"Perjantain kasaus (pe klo 14-18)", None),
            (u"Lauantain aamuvuoro (la klo 08-11)", None),
            (u"Lauantain päivävuoro (la klo 11-15)", None),
            (u"Lauantain iltapäivävuoro (la klo 15-18)", None),
            (u"Sunnuntain aamuvuoro (su klo 08-11)", None),
            (u"Sunnuntain päivävuoro (su klo 11-15)", None),
            (u"Sunnuntain purkuvuoro (su klo 15-17)", None),
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

        AlternativeSignupForm.objects.get_or_create(
            event=self.event,
            slug=u'kuplitea',
            defaults=dict(
                title=u'Kuplitean ilmoittautumislomake',
                signup_form_class_path='kuplii2015.forms:OrganizerSignupForm',
                signup_extra_form_class_path='kuplii2015.forms:OrganizerSignupExtraForm',
                active_from=datetime(2015, 1, 21, 22, 0, 0, tzinfo=self.tz),
                active_until=self.event.end_time,
            ),
        )

        for wiki_space, link_title, link_group in [
            ('KUPLIIWORK', 'Työvoimawiki', 'accepted'),
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
    help = 'Setup kuplii2015 specific stuff'

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
