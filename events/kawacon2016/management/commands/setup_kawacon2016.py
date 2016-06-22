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
        from core.models import Organization, Venue, Event

        self.organization, unused = Organization.objects.get_or_create(slug='kawacon-ry', defaults=dict(
            name='Kawacon ry',
            homepage_url='http://www.kawacon.info',
        ))
        self.venue, unused = Venue.objects.get_or_create(name='Peltolan ammattiopisto', defaults=dict(
            name_inessive='Peltolan ammattiopistolla' # XXX not really inessive
        ))
        self.event, unused = Event.objects.get_or_create(slug='kawacon2016', defaults=dict(
            name='Kawacon (2016)',
            name_genitive='Kawaconin',
            name_illative='Kawaconiin',
            name_inessive='Kawaconissa',
            homepage_url='http://www.kawacon.info',
            organization=self.organization,
            start_time=datetime(2016, 7, 2, 10, 0, tzinfo=self.tz),
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
        from ...models import SpecialDiet, SignupExtra, Night
        from django.contrib.contenttypes.models import ContentType

        labour_admin_group, = LabourEventMeta.get_or_create_groups(self.event, ['admins'])

        if self.test:
            from core.models import Person
            person, unused = Person.get_or_create_dummy()
            labour_admin_group.user_set.add(person.user)

        content_type = ContentType.objects.get_for_model(SignupExtra)

        labour_event_meta_defaults = dict(
            signup_extra_content_type=content_type,
            work_begins=datetime(2016, 7, 1, 7, 0, tzinfo=self.tz),
            work_ends=datetime(2016, 7, 4, 16, 0, tzinfo=self.tz),
            admin_group=labour_admin_group,
            contact_email='Kawacon <mitro.makkonen@gmail.com>',
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

        for pc_name, pc_slug, pc_app_label in [
            (u'Conitea', 'conitea', 'labour'),
            (u'Vänkäri', 'tyovoima', 'labour'),
            (u'Ohjelmanjärjestäjä', 'ohjelma', 'programme'),
            (u'Myyjä', 'myyja', 'badges'),
            (u'Vieras', 'vieras', 'badges'),
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
        ohjelma = PersonnelClass.objects.get(event=self.event, slug='ohjelma')

        for jc_data in [
            (u'Conitea', u'Tapahtuman järjestelytoimikunnan eli conitean jäsen', [conitea]),

            (u'Siisteys & Somistus', u'Conin siistinä pitäminen, vesipisteiden täyttäminen ja conipaikan koristelu. Tehtävä ei vaadi erityisosaamista. Tämä tehtävä sopii hyvin ensikertalaisvänkäreille.', [tyovoima]),
            (u'Logistiikka', u'Autokuskina toimimista ja tavaroiden/ihmisten hakua ja noutamista. Tehtäviä on perjantaina ja sunnuntai-iltana. Edellyttää B-ajokorttia. Jos sinulla on oma auto ja olet valmis käyttämään sitä conissa, mainitse siitä Vapaa alue-kentässä.', [tyovoima]),
            (u'Majoitus', u'Majoitusvänkärit huolehtivat lattiamajoituspaikkojen pyörittämisestä yöaikaan.', [tyovoima]),
            (u'Järjestyksenvalvonta', u'Kävijöiden turvallisuuden valvominen conipaikalla. Edellyttää voimassa olevaa JV-korttia ja asiakaspalveluasennetta. HUOM! Et voi valita tätä tehtävää hakemukseesi, ellet ole täyttänyt tietoihisi JV-kortin numeroa (oikealta ylhäältä oma nimesi &gt; Pätevyydet).', [tyovoima]),
            (u'Ensiapu', u'Ensiapupäivystys tapahtumapaikalla. Edellyttää voimassa olevaa ensiapukorttia (vähintään EA1).', [tyovoima]),
            (u'Green room', u'Työvoiman taukohuoneen hoitaminen ja kahvin keitto green roomissa. Hygieniapassin omistaminen on suositeltavaa, mutta ei välttämätöntä.', [tyovoima]),
            (u'Keittiö & kahvio', u'Ruuan valmistus keittiössä, sekä asiakaspalvelu kahviossa. Hygieniapassin omistaminen on suositeltavaa, mutta voit ilmoittautua kahvioon ilmankin.', [tyovoima]),
            (u'Info ja narikka', u'Infopisteen henkilökunta vastaa kävijöiden kysymyksiin ja ratkaisee heidän ongelmiaan tapahtuman aikana. Narikka toimii infon yhteydessä. Tehtävä edellyttää asiakaspalveluasennetta, tervettä järkeä ja ongelmanratkaisukykyä.', [tyovoima]),
            (u'Lipunmyynti', u'Pääsylippujen myyntiä. Myyjiltä edellytetään asiakaspalveluhenkeä, päässälaskutaitoa ja huolellisuutta rahankäsittelyssä.', [tyovoima]),
            (u'Meido', u'Meidokahvilassa työskentely. Asiakkaille tarjoileminen, sekä asiakkaille seuran pitäminen. Ilmoittaudu tähän tehtävään vain jos meidovastaava on hyväksynyt sinuterillishaussa. Meidohaku löytyy <a href="http://www.kawacon.info" target="_blank">Kawaconin kotisivuilta</a>.', [tyovoima]),
            (u'Ohjelmavänkäri', u'Tähän vänkäriryhmään tulevat salivänkärit, ohjelma-avustajat ja Kawaplayn lautapelivuokraamon vänkärit. Tehtävät eivät edellytä erikoisosaamista. Jos sinulla on kokemusta salitekniikasta, voit mainita tästä Vapaa alue-kentässä.', [tyovoima]),
            (u'Erikoistehtävä', u'Mikäli olet sopinut erikseen työtehtävistä ja/tai sinut on ohjeistettu täyttämään lomake, valitse tämä ja kerro tarkemmin Vapaa alue -kentässä mihin tehtävään ja kenen toimesta sinut on valittu.', [tyovoima]),
            (u'Rakennus ja purku', u'Conipaikan rakennus, pöytien järjestely ja raskaiden esineiden kantaminen. Tehtävät ajoittuvat perjantaille ja sunnuntai-illalle.', [tyovoima]),
            (u'Kuvaus', 'Valokuvaus ja coniviikonlopun ikuistaminen. Tehtävä edellyttää kameraa ja mahdollisuutta kuvien jälkikäsittelyyn. Kerro Vapaa alue-kentässä millaisen kameran omistat ja aiemmasta kuvauskokemuksestasi.', [tyovoima]),

            # (u'Ohjelmanpitäjä', u'Luennon tai muun vaativan ohjelmanumeron pitäjä', [ohjelma]),
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

        for name in [u'Conitea']:
            JobCategory.objects.filter(event=self.event, name=name).update(public=False)

        for jc_name, qualification_name in [
            (u'Järjestyksenvalvonta', u'JV-kortti'),
            # (u'Green room', u'Hygieniapassi'),
            (u'Ensiapu', u'Ensiapukoulutus EA1'),
        ]:
            jc = JobCategory.objects.get(event=self.event, name=jc_name)
            qual = Qualification.objects.get(name=qualification_name)
            if not jc.required_qualifications.exists():
                jc.required_qualifications = [qual]
                jc.save()

        for diet_name in [
            u'Gluteeniton',
            u'Laktoositon',
            u'Maidoton',
            # u'Vegaaninen',
            # u'Lakto-ovo-vegetaristinen',
        ]:
            SpecialDiet.objects.get_or_create(name=diet_name)

        for night in [
            u'Perjantain ja lauantain välinen yö',
            u'Lauantain ja sunnuntain välinen yö',
            u'Sunnuntain ja maanantain välinen yö',
        ]:
            Night.objects.get_or_create(name=night)

        AlternativeSignupForm.objects.get_or_create(
            event=self.event,
            slug=u'conitea',
            defaults=dict(
                title=u'Conitean ilmoittautumislomake',
                signup_form_class_path='events.kawacon2016.forms:OrganizerSignupForm',
                signup_extra_form_class_path='events.kawacon2016.forms:OrganizerSignupExtraForm',
                active_from=datetime(2015, 12, 3, 0, 0, 0, tzinfo=self.tz),
                active_until=self.event.end_time,
            ),
        )

    def setup_programme(self):
        from programme.models import Room, ProgrammeEventMeta, Category, TimeBlock, View, SpecialStartTime
        from core.utils import full_hours_between

        room_order = 0
        for room_name in [
            # u'Auditorio',
            # u'Pääsali',
            # u'E-rakennus, luokat',
            # u'Kawaplay, G-rakennus',
            # u'Elokuvateatteri Tapio',
        ]:
            room_order += 100
            Room.objects.get_or_create(
                venue=self.venue,
                name=room_name,
                defaults=dict(
                    order=room_order,
                )
            )

        admin_group, hosts_group = ProgrammeEventMeta.get_or_create_groups(self.event, ['admins', 'hosts'])
        programme_event_meta, unused = ProgrammeEventMeta.objects.get_or_create(event=self.event, defaults=dict(
            admin_group=admin_group,
        ))

        view, unused = View.objects.get_or_create(
            event=self.event,
            name='Ohjelmakartta',
        )

        if not view.rooms.exists():
            view.rooms = Room.objects.filter(venue=self.venue, active=True)
            view.save()

        for category_name, category_style in [
            # (u'Luento', u'anime'),
            # (u'Non-stop', u'miitti'),
            (u'Työpaja', u'rope'),
            (u'Muu ohjelma', u'muu'),
            # (u'Show', u'cosplay'),
        ]:
            Category.objects.get_or_create(
                event=self.event,
                title=category_name,
                defaults=dict(
                    style=category_style,
                )
            )

        for start_time, end_time in [
            (
                self.event.start_time,
                self.event.start_time.replace(hour=18),
            ),
            (
                self.event.end_time.replace(hour=10),
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

            # <Kharnis> Lisäksi, saapiko ohjelmakartan toimimaan 30 min tarkkuudella?
            # [:-1] – discard 18:30
            for hour_start_time in full_hours_between(start_time, end_time)[:-1]:
                SpecialStartTime.objects.get_or_create(
                    event=self.event,
                    start_time=hour_start_time.replace(minute=30)
                )


class Command(BaseCommand):
    args = ''
    help = 'Setup kawacon2016 specific stuff'

    def handle(self, *args, **opts):
        Setup().setup(test=settings.DEBUG)
