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

    def setup_core(self):
        from core.models import Venue, Event

        self.venue, unused = Venue.objects.get_or_create(name='Sipoon Topeliussali', defaults=dict(
            name_inessive='Sipoon Topeliussalissa',
        ))
        self.event, unused = Event.objects.get_or_create(slug='shippocon2016', defaults=dict(
            name='Shippocon (2016)',
            name_genitive='Shippoconin',
            name_illative='Shippoconiin',
            name_inessive='Shippoconissa',
            homepage_url='http://shippocon.fi',
            organization_name='Laura Sinkkonen',
            organization_url='http://shippocon.fi',
            start_time=datetime(2016, 9, 24, 10, 0, tzinfo=self.tz),
            end_time=datetime(2016, 9, 24, 18, 0, tzinfo=self.tz),
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
            work_begins=datetime(2016, 9, 23, 14, 0, tzinfo=self.tz),
            work_ends=datetime(2016, 9, 24, 20, 0, tzinfo=self.tz),
            admin_group=labour_admin_group,
            contact_email='Shippoconin työvoimavastaava <shippocon.vankarit@gmail.com>',
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
            ('Pääjärjestäjä', 'pj', 'labour'),
            ('Vastaava', 'vastaava', 'labour'),
            ('Työvoima', 'tyovoima', 'labour'),
            ('Myyjä', 'myyja', 'badges'),
            ('Vieras', 'vieras', 'badges'),
            ('Media', 'media', 'badges'),
            ('Ohjelmanjärjestäjä', 'ohjelma', 'programme'),
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
        vastaava = PersonnelClass.objects.get(event=self.event, slug='vastaava')
        ohjelma = PersonnelClass.objects.get(event=self.event, slug='ohjelma')

        for name, description, pcs in [
            ('Vastaava', 'Tapahtuman järjestelytoimikunnan jäsen eli vastaava', [vastaava]),

            ('Erikoistehtävä', 'Mikäli olet sopinut erikseen työtehtävistä ja/tai sinut on ohjeistettu täyttämään lomake, valitse tämä ja kerro tarkemmin Vapaa alue -kentässä mihin tehtävään ja kenen toimesta sinut on valittu.', [tyovoima]),
            ('Järjestyksenvalvoja', 'Kävijöiden turvallisuuden valvominen conipaikalla. Edellyttää voimassa olevaa JV-korttia ja asiakaspalveluasennetta. HUOM! Et voi valita tätä tehtävää hakemukseesi, ellet ole täyttänyt tietoihisi JV-kortin numeroa (oikealta ylhäältä oma nimesi > Pätevyydet).', [tyovoima]),
            ('Ensiapu', 'Toimit osana tapahtuman omaa ensiapuryhmää. Vaaditaan vähintään voimassa oleva EA1 -kortti', [tyovoima]),
            ('Salivänkäri', 'Salivänkäri vastaa ohjelmasalien toiminnasta. He pitävät huolen, että ohjelmat alkavat ja loppuvat ajallaan ja että ohjelmanjärjestäjillä on kaikki mitä he tarvitsevat salissa.', [tyovoima]),
            ('Tekniikka', 'Tekniikkavänkärit huolehtivat tapahtuman aikana teknologian toimivuudesta. Työtehtävät ovat hyvin monipuolisia jatkojohtojen toimittamisesta ohjelmansalien äänentoistosta huolehtimiseen, joten tietotekniikan laaja perustuntemus on valinnan edellytyksenä.', [tyovoima]),
            ('Yleisvänkäri', 'Sekalaisia tehtäviä laidasta laitaan, jotka eivät vaadi erikoisosaamista. Voit halutessasi kirjata lisätietoihin, mitä osaat ja haluaisit tehdä.', [tyovoima]),
            ('Info', 'Infopisteen henkilökunta vastaa kävijöiden kysymyksiin ja ratkaisee heidän ongelmiaan tapahtuman paikana. Tehtävä edellyttää asiakaspalveluasennetta, tervettä järkeä ja ongelmanratkaisukykyä.', [tyovoima]),
            ('Cosplaymamma', 'Cosplaykisaajien avustamista backstagella. Kerro Vapaa alue -kentässä aiemmasta kisakokemuksestasi backstagelta/kisaajana/cosplaymammana. Missä, milloin ja montako kertaa olet tehnyt mammaduunia?', [tyovoima]),
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

        for name in [u'Vastaava']:
            JobCategory.objects.filter(event=self.event, name=name).update(public=False)

        for jc_name, qualification_name in [
            ('Järjestyksenvalvoja', 'JV-kortti'),
        ]:
            jc = JobCategory.objects.get(event=self.event, name=jc_name)
            qual = Qualification.objects.get(name=qualification_name)

            jc.required_qualifications = [qual]
            jc.save()

        for diet_name in [
            u'Gluteeniton',
            u'Laktoositon',
            u'Maidoton',
            u'Vegaaninen',
            u'Lakto-ovo-vegetaristinen',
        ]:
            SpecialDiet.objects.get_or_create(name=diet_name)

        AlternativeSignupForm.objects.get_or_create(
            event=self.event,
            slug=u'vastaava',
            defaults=dict(
                title=u'Vastaavan ilmoittautumislomake',
                signup_form_class_path='events.shippocon2016.forms:OrganizerSignupForm',
                signup_extra_form_class_path='events.shippocon2016.forms:OrganizerSignupExtraForm',
                active_from=datetime(2016, 6, 23, 0, 0, 0, tzinfo=self.tz),
                active_until=self.event.end_time,
            ),
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


class Command(BaseCommand):
    args = ''
    help = 'Setup shippocon2016 specific stuff'

    def handle(self, *args, **opts):
        Setup().setup(test=settings.DEBUG)
