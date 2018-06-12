from datetime import datetime, timedelta

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.timezone import now

from dateutil.tz import tzlocal


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

        self.organization, unused = Organization.objects.get_or_create(slug='tutka', defaults=dict(
            name='Tracon ry',
            homepage_url='https://ry.tracon.fi/',
        ))
        self.venue, unused = Venue.objects.get_or_create(name='Ilmoitetaan myöhemmin', defaults=dict(
            name_inessive='Ilmoitetaan myöhemmin',
        ))
        self.event, unused = Event.objects.get_or_create(slug='concon16', defaults=dict(
            name='Concon 16',
            name_genitive='Concon 16 -seminaarin',
            name_illative='Concon 16 -seminaariin',
            name_inessive='Concon 16 -seminaarissa',
            homepage_url='https://con2.fi/concon',
            organization=self.organization,
            start_time=datetime(2018, 11, 3, 10, 0, tzinfo=self.tz),
            end_time=datetime(2018, 11, 3, 18, 0, tzinfo=self.tz),
            venue=self.venue,
        ))

    def setup_enrollment(self):
        from enrollment.models import (
            EnrollmentEventMeta,
            SpecialDiet,
            ConconPart,
        )

        enrollment_admin_group, = EnrollmentEventMeta.get_or_create_groups(self.event, ['admins'])

        enrollment_event_meta_defaults = dict(
            admin_group=enrollment_admin_group,
            form_class_path='events.concon16.forms:EnrollmentForm',
            is_participant_list_public=True,
        )

        if self.test:
            enrollment_event_meta_defaults.update(
                enrollment_opens=now() - timedelta(days=60),
                enrollment_closes=now() + timedelta(days=60),
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

        for part_name in [
            'Luento-ohjelma',
            'Jatkot',
        ]:
            ConconPart.objects.get_or_create(name=part_name)


class Command(BaseCommand):
    args = ''
    help = 'Setup Concon 16 specific stuff'

    def handle(self, *args, **opts):
        Setup().setup(test=settings.DEBUG)
