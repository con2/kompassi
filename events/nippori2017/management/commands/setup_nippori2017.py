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
        self.setup_programme()
        self.setup_badges()

    def setup_core(self):
        from core.models import Venue, Event

        self.venue, unused = Venue.objects.get_or_create(name='Porin kaupunginkirjasto ja keskustan nuorisotalo', defaults=dict(
            name_inessive='Porin kaupunginkirjastossa ja keskustan nuorisotalolla',
        ))
        self.event, unused = Event.objects.get_or_create(slug='nippori2017', defaults=dict(
            name='Nippori (2017)',
            name_genitive='Nipporin',
            name_illative='Nipporiin',
            name_inessive='Nipporissa',
            homepage_url='http://nipporipori.blogspot.fi/',
            organization_name='Porin kaupunginkirjasto',
            organization_url='http://www.pori.fi/kirjasto',
            start_time=datetime(2017, 9, 30, 12, 0, tzinfo=self.tz),
            end_time=datetime(2017, 9, 30, 21, 0, tzinfo=self.tz),
            venue=self.venue,
        ))

    def setup_programme(self):
        from labour.models import PersonnelClass
        from programme.models import (
            Category,
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
            # kirjasto
            'Aikuistenosasto',
            'Lastenosasto',
            'Kellari',
            'Kahvila',
            'Seminaarihuone 1',

            # nuokkari
            'Iso sali',
            'Pikkusali',
            'Alakerta',
            'Aula',
            'Kerhohuone 2',
            'Kerhohuone 3',
            'Kerhohuone 4',
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
            programme_event_meta.contact_email = 'Nippori <siina.vieri@pori.fi>'
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

        for view_name, room_names in [
            ('Kirjasto', [
                'Aikuistenosasto',
                'Lastenosasto',
                'Kellari',
                'Kahvila',
                'Seminaarihuone 1',
            ]),
            ('Nuokkari', [
                'Iso sali',
                'Pikkusali',
                'Alakerta',
                'Aula',
                'Kerhohuone 2',
                'Kerhohuone 3',
                'Kerhohuone 4',
            ]),
        ]:
            view, unused = View.objects.get_or_create(
                event=self.event,
                name=view_name,
            )

            if not view.rooms.exists():
                view.rooms = Room.objects.filter(venue=self.venue, active=True, name__in=room_names)
                view.save()

        for category_name, category_style in [
            ('Anime ja manga', 'color1'),
            ('Cosplay', 'color2'),
            ('Japanin kulttuuri', 'color3'),
            ('Työpaja', 'color4'),
            ('Muu ohjelma', 'color5'),
        ]:
            Category.objects.get_or_create(
                event=self.event,
                title=category_name,
                defaults=dict(
                    style=category_style,
                )
            )

        for tag_name, tag_style in [
            ('Suositeltu', 'hilight'),
        ]:
            Tag.objects.get_or_create(
                event=self.event,
                title=tag_name,
                defaults=dict(
                    style=tag_style,
                ),
            )

        if not TimeBlock.objects.filter(event=self.event).exists():
            for start_time, end_time in [
                (
                    self.event.start_time,
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

        for time_block in TimeBlock.objects.filter(event=self.event):
            # Half hours
            # [:-1] – discard 18:30
            for hour_start_time in full_hours_between(time_block.start_time, time_block.end_time)[:-1]:
                SpecialStartTime.objects.get_or_create(
                    event=self.event,
                    start_time=hour_start_time.replace(minute=30)
                )

    def setup_labour(self):
        from core.models import Person
        from labour.models import (
            Job,
            JobCategory,
            LabourEventMeta,
            PersonnelClass,
            Qualification,
        )
        from ...models import SignupExtra
        from django.contrib.contenttypes.models import ContentType

        labour_admin_group, = LabourEventMeta.get_or_create_groups(self.event, ['admins'])

        if self.test:
            person, unused = Person.get_or_create_dummy()
            labour_admin_group.user_set.add(person.user)

        content_type = ContentType.objects.get_for_model(SignupExtra)

        labour_event_meta_defaults = dict(
            signup_extra_content_type=content_type,
            work_begins=self.event.start_time,
            work_ends=self.event.end_time + timedelta(hours=1),
            admin_group=labour_admin_group,
            contact_email='Nippori <siina.vieri@pori.fi>',
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
            ('Työryhmä', 'tyoryhma', 'labour'),
            ('Ohjelmanjärjestäjä', 'ohjelma', 'programme'),
            ('Myyjä/yhdistys', 'myyja-yhdistys', 'badges'),
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

        tyoryhma = PersonnelClass.objects.get(event=self.event, slug='tyoryhma')

        for jc_data in [
            (
                'Työryhmä',
                'Tapahtuman työryhmän jäsen',
                [tyoryhma]
            ),
            (
                'Järjestyksenvalvoja',
                'Kävijöiden turvallisuuden valvominen conipaikalla ja yömajoituksessa. Edellyttää voimassa olevaa '
                'JV-korttia ja asiakaspalveluasennetta. HUOM! Et voi valita tätä tehtävää hakemukseesi, ellet ole '
                'täyttänyt tietoihisi JV-kortin numeroa (oikealta ylhäältä oma nimesi &gt; Pätevyydet).',
                [tyoryhma],
            ),
            (
                'Kirpputori',
                '',
                [tyoryhma],
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

        for jc_name, qualification_name in [
            ('Järjestyksenvalvoja', 'JV-kortti'),
        ]:
            jc = JobCategory.objects.get(event=self.event, name=jc_name)
            qual = Qualification.objects.get(name=qualification_name)
            if not jc.required_qualifications.exists():
                jc.required_qualifications = [qual]
                jc.save()

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
    help = 'Setup nippori2017 specific stuff'

    def handle(self, *args, **opts):
        Setup().setup(test=settings.DEBUG)
