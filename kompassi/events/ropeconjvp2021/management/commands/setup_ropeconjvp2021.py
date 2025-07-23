from datetime import datetime

from dateutil.tz import tzlocal
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **opts):
        from kompassi.core.models import Event, Organization, Venue
        from kompassi.zombies.enrollment.models import EnrollmentEventMeta

        tz = tzlocal()
        organization = Organization.objects.get(slug="ropecon-ry")
        venue, unused = Venue.objects.get_or_create(
            name="Ilmoitetaan myöhemmin",
            defaults=dict(
                name_inessive="Ilmoitetaan myöhemmin",
            ),
        )
        event, unused = Event.objects.get_or_create(
            slug="ropeconjvp2021",
            defaults=dict(
                public=False,
                name="Ropeconin JV-peruskurssi 2021",
                name_genitive="Ropeconin JV-peruskurssin",
                name_illative="Ropeconin JV-peruskurssille",
                name_inessive="Ropeconin JV-peruskurssilla",
                homepage_url="http://ropecon.fi/hallitus",
                organization=organization,
                start_time=datetime(2021, 8, 9, 11, 0, tzinfo=tz),
                end_time=datetime(2021, 8, 15, 19, 0, tzinfo=tz),
                venue=venue,
            ),
        )

        (admin_group,) = EnrollmentEventMeta.get_or_create_groups(event, ["admins"])

        EnrollmentEventMeta.objects.get_or_create(
            event=event,
            defaults=dict(
                admin_group=admin_group,
                form_class_path="events.ropeconjvp2021.forms:EnrollmentForm",
                is_participant_list_public=False,
                is_official_name_required=True,
            ),
        )
