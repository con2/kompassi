from datetime import datetime

from django.core.management.base import BaseCommand

from dateutil.tz import tzlocal


class Command(BaseCommand):
    def handle(self, *args, **opts):
        from core.models import Event, Organization, Venue
        from enrollment.models import EnrollmentEventMeta

        tz = tzlocal()
        organization = Organization.objects.get(slug='tracon-ry')
        venue, unused = Venue.objects.get_or_create(name='Ilmoitetaan myöhemmin', defaults=dict(
            name_inessive='Ilmoitetaan myöhemmin',
        ))
        event, unused = Event.objects.get_or_create(
            slug='traconjvp2019',
            defaults=dict(
                public=False,
                name='Traconin JV-peruskurssi 2019',
                name_genitive='Traconin JV-peruskurssin',
                name_illative='Traconin JV-peruskurssille',
                name_inessive='Traconin JV-peruskurssilla',
                homepage_url='http://ry.tracon.fi/',
                organization=organization,
                start_time=datetime(2019, 4, 13, 10, 0, tzinfo=tz),
                end_time=datetime(2019, 4, 13, 22, 0, tzinfo=tz),
                venue=venue,
            )
        )

        admin_group, = EnrollmentEventMeta.get_or_create_groups(event, ['admins'])

        EnrollmentEventMeta.objects.get_or_create(
            event=event,
            defaults=dict(
                admin_group=admin_group,
                form_class_path='events.traconjvp2019.forms:EnrollmentForm',
                is_participant_list_public=False,
                is_official_name_required=True,
            ),
        )
