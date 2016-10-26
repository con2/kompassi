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
        self.setup_access()
        self.setup_programme()

    def setup_core(self):
        from core.models import Venue, Event

        self.venue, unused = Venue.objects.get_or_create(name='Malmitalo', defaults=dict(
            name_inessive='Malmitalolla',
        ))
        self.event, unused = Event.objects.get_or_create(slug='tylycon2017', defaults=dict(
            name='Tylycon (2017)',
            name_genitive='Tylyconin',
            name_illative='Tylyconiin',
            name_inessive='Tylyconissa',
            homepage_url='http://tylycon.fi',
            organization_name='Luutakomero ry',
            organization_url='http://tylycon.fi',
            start_time=datetime(2017, 4, 8, 10, 0, tzinfo=self.tz),
            end_time=datetime(2017, 4, 8, 18, 0, tzinfo=self.tz),
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
            work_begins=self.event.start_time - timedelta(days=1),
            work_ends=self.event.end_time + timedelta(hours=4),
            admin_group=labour_admin_group,
            contact_email='Tylyconin työvoimatiimi <tyovoima@tylycon.fi>',
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
            ('Ohjelmanjärjestäjä', 'ohjelma', 'programme'),
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

        # tyovoima = PersonnelClass.objects.get(event=self.event, slug='tyovoima')
        conitea = PersonnelClass.objects.get(event=self.event, slug='conitea')

        for jc_data in [
            (
                'Conitea',
                'Tapahtuman järjestelytoimikunnan eli conitean jäsen',
                [conitea]
            ),
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
            slug='conitea',
            defaults=dict(
                title='Conitean ilmoittautumislomake',
                signup_form_class_path='events.tylycon2017.forms:OrganizerSignupForm',
                signup_extra_form_class_path='events.tylycon2017.forms:OrganizerSignupExtraForm',
                active_from=datetime(2016, 5, 16, 12, 0, 0, tzinfo=self.tz),
                active_until=self.event.start_time,
            ),
        )

        for wiki_space, link_title, link_group in [
            # ('TYLYWORK', 'Työvoimawiki', 'accepted'),
            # ('TYLYINFO', 'Infowiki', 'info'),
        ]:
            InfoLink.objects.get_or_create(
                event=self.event,
                title=link_title,
                defaults=dict(
                    url='https://confluence.tracon.fi/display/{wiki_space}'.format(wiki_space=wiki_space),
                    group=labour_event_meta.get_group(link_group),
                )
            )

    def setup_access(self):
        from access.models import Privilege, GroupPrivilege, EmailAliasType, GroupEmailAliasGrant

        cc_group = self.event.labour_event_meta.get_group('conitea')

        for metavar in [
            'etunimi.sukunimi',
            'nick',
        ]:
            alias_type = EmailAliasType.objects.get(domain__domain_name='tylycon.fi', metavar=metavar)
            GroupEmailAliasGrant.objects.get_or_create(
                group=cc_group,
                type=alias_type,
                defaults=dict(
                    active_until=self.event.end_time,
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
            Tag,
            TimeBlock,
            View,
        )
        from core.utils import full_hours_between

        for room_name in [
            'Suuri sali',
            'Tarvehuone',
            'Tähtitorni',
            'Loitsuluokka',
            'Kasvihuone 3',
            'Salaisuuksien kammio',
        ]:
            Room.objects.get_or_create(
                venue=self.venue,
                name=room_name,
                defaults=dict(
                    order=self.get_ordering_number(),
                )
            )

        admin_group, hosts_group = ProgrammeEventMeta.get_or_create_groups(self.event, ['admins', 'hosts'])
        programme_event_meta, unused = ProgrammeEventMeta.objects.get_or_create(event=self.event, defaults=dict(
            admin_group=admin_group,
        ))

        if not programme_event_meta.contact_email:
            programme_event_meta.contact_email = 'Tylyconin ohjelmavastaava <ohjelma@tylycon.fi>'
            programme_event_meta.save()

        if settings.DEBUG:
            programme_event_meta.accepting_cold_offers_from = now() - timedelta(days=60)
            programme_event_meta.accepting_cold_offers_until = now() + timedelta(days=60)
            programme_event_meta.save()

        for pc_slug, role_title, role_is_default in [
            ('ohjelma', 'Ohjelmanjärjestäjä', True),
        ]:
            personnel_class = PersonnelClass.objects.get(event=self.event, slug=pc_slug)
            role, unused = Role.objects.get_or_create(
                personnel_class=personnel_class,
                title=role_title,
                defaults=dict(
                    is_default=role_is_default,
                )
            )

        view, unused = View.objects.get_or_create(
            event=self.event,
            name='Ohjelmakartta',
        )

        if not view.rooms.exists():
            view.rooms = Room.objects.filter(venue=self.venue, active=True)
            view.save()

        for category_name, category_style in [
            ('Puheohjelma', 'color1'),
            ('Keskusteluohjelma', 'color2'),
            ('Työpaja', 'color3'),
            ('Muu ohjelma', 'color4'),
        ]:
            Category.objects.get_or_create(
                event=self.event,
                title=category_name,
                defaults=dict(
                    style=category_style,
                )
            )

        for tag_name, tag_style in [
        ]:
            Tag.objects.get_or_create(
                event=self.event,
                title=tag_name,
                defaults=dict(
                    style=tag_style,
                ),
            )

        TimeBlock.objects.get_or_create(
            event=self.event,
            start_time=self.event.start_time,
            defaults=dict(
                end_time=self.event.end_time,
            ),
        )

        # Half hours
        # [:-1] – discard 18:30
        # for hour_start_time in full_hours_between(start_time, end_time)[:-1]:
        #     SpecialStartTime.objects.get_or_create(
        #         event=self.event,
        #         start_time=hour_start_time.replace(minute=30)
        #     )


class Command(BaseCommand):
    args = ''
    help = 'Setup tylycon2017 specific stuff'

    def handle(self, *args, **opts):
        Setup().setup(test=settings.DEBUG)
