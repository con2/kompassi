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

    def setup_core(self):
        from core.models import Venue, Event

        self.venue, unused = Venue.objects.get_or_create(name='Messukeskus', defaults=dict(
            name_inessive='Messukeskuksessa',
        ))
        self.event, unused = Event.objects.get_or_create(slug='worldcon75', defaults=dict(
            name='Worldcon 75',
            name_genitive='Worldcon 75 -tapahtuman',
            name_illative='Worldcon 75 -tapahtumaan',
            name_inessive='Worldcon 75 -tapahtumassa',
            homepage_url='http://www.worldcon.fi',
            organization_name='Maa ja ilma ry',
            organization_url='http://www.worldcon.fi',
            start_time=datetime(2017, 8, 9, 9, 0, tzinfo=self.tz),
            end_time=datetime(2017, 8, 13, 18, 0, tzinfo=self.tz),
            venue=self.venue,
        ))

    def setup_labour(self):
        from core.models import Person
        from labour.models import (
            AlternativeSignupForm,
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
            work_begins=self.event.start_time - timedelta(days=1),
            work_ends=self.event.end_time + timedelta(hours=4),
            admin_group=labour_admin_group,
            contact_email='Popcult Helsingin työvoimavastaava <virve.honkala@popcult.fi>',
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
            ('Järjestyksenvalvoja', 'jv', 'labour'),
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

        jv = PersonnelClass.objects.get(event=self.event, slug='jv')

        for jc_data in [
            (
                'Järjestyksenvalvoja',
                (
                    'Worldcon 75 hakee Kompassin kautta ainoastaan järjestyksenvalvojia. '
                    'Mikäli kortillisia järjestyksenvalvojia ei saada tarpeeksi, heitä voidaan myös kouluttaa. '
                    'Mikäli sinulla on JV-kortti, muistathan täyttää sen numeron '
                    '<a href="/profile/qualifications" target="_blank">profiiliisi</a>. '
                    'Ilmoita myös, jos sinulla on ensiapukortti.'
                ),
                [jv]
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
            # ('Järjestyksenvalvoja', 'JV-kortti'), # no!
        ]:
            jc = JobCategory.objects.get(event=self.event, name=jc_name)
            qual = Qualification.objects.get(name=qualification_name)
            if not jc.required_qualifications.exists():
                jc.required_qualifications = [qual]
                jc.save()


class Command(BaseCommand):
    args = ''
    help = 'Setup worldcon75 specific stuff'

    def handle(self, *args, **opts):
        Setup().setup(test=settings.DEBUG)
