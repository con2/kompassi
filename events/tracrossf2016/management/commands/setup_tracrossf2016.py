# encoding: utf-8



import os
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
        self.setup_enrollment()

    def setup_core(self):
        from core.models import Organization, Venue, Event

        self.organization, unused = Organization.objects.get_or_create(slug='tracon-ry', defaults=dict(
            name='Tracon ry',
            homepage_url='https://ry.tracon.fi',
        ))
        self.venue, unused = Venue.objects.get_or_create(name='Akun Tehdas', defaults=dict(
            name_inessive='Akun Tehtaalla', # not actually inessive lol
        ))
        self.event, unused = Event.objects.get_or_create(slug='tracrossf2016', defaults=dict(
            name='Tracross Frontier (2016)',
            name_genitive='Tracross Frontierin',
            name_illative='Tracross Frontieriin',
            name_inessive='Tracross Frontierissa',
            homepage_url='https://r.tracon.fi/tracrossf',
            organization=self.organization,
            start_time=datetime(2016, 10, 22, 12, 0, tzinfo=self.tz),
            end_time=datetime(2016, 10, 22, 22, 0, tzinfo=self.tz),
            venue=self.venue,
        ))

    def setup_enrollment(self):
        from enrollment.models import (
            EnrollmentEventMeta,
            SpecialDiet,
        )

        enrollment_admin_group, = EnrollmentEventMeta.get_or_create_groups(self.event, ['admins'])

        enrollment_event_meta_defaults = dict(
            admin_group=enrollment_admin_group,
            form_class_path='events.tracrossf2016.forms:EnrollmentForm',
        )

        if self.test:
            enrollment_event_meta_defaults.update(
                enrollment_opens=now() - timedelta(days=60),
                enrollment_closes=now() + timedelta(days=60),
            )
        else:
            enrollment_event_meta_defaults.update(
                enrollment_opens=datetime(2016, 10, 11, 20, 10, 0, tzinfo=self.tz),
                enrollment_closes=datetime(2016, 10, 20, 23, 59, 59, tzinfo=self.tz),
            )

        enrollment_event_meta, unused = EnrollmentEventMeta.objects.get_or_create(
            event=self.event,
            defaults=enrollment_event_meta_defaults,
        )

        for diet_name in [
            'Gluteeniton',
            'Laktoositon',
            'Maidoton',
            'Vegaaninen',
            'Lakto-ovo-vegetaristinen',
        ]:
            SpecialDiet.objects.get_or_create(name=diet_name)


class Command(BaseCommand):
    args = ''
    help = 'Setup Tracross Frontier 2016 specific stuff'

    def handle(self, *args, **opts):
        Setup().setup(test=settings.DEBUG)
