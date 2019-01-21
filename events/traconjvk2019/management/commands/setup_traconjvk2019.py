from datetime import datetime

from django.core.management.base import BaseCommand

from dateutil.tz import tzlocal


class Command(BaseCommand):
    def handle(self, *args, **opts):
        from core.models import Event, Organization, Venue
        from enrollment.models import EnrollmentEventMeta

        tz = tzlocal()
        organization = Organization.objects.get(slug='tracon-ry'    )
        venue, unused = Venue.objects.get_or_create(name='Ilmoitetaan myöhemmin')
        event, unused = Event.objects.get_or_create(
            slug='traconjvk2019',
            defaults=dict(
                public=False,
                name='Traconin JV-kertauskurssi 2019',
                name_genitive='Traconin JV-kertauskurssin',
                name_illative='Traconin JV-kertauskurssille',
                name_inessive='Traconin JV-kertauskurssilla',
                homepage_url='http://ry.tracon.fi/',
                organization=organization,
                start_time=datetime(2019, 2, 24, 10, 0, tzinfo=tz),
                end_time=datetime(2019, 2, 24, 22, 0, tzinfo=tz),
                venue=venue,
            )
        )

        admin_group, = EnrollmentEventMeta.get_or_create_groups(event, ['admins'])

        EnrollmentEventMeta.objects.get_or_create(
            event=event,
            defaults=dict(
                admin_group=admin_group,
                form_class_path='events.traconjvk2019.forms:EnrollmentForm',
                is_participant_list_public=False,
                is_official_name_required=True,
            ),
        )
