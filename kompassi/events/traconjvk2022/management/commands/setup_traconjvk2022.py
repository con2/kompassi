from datetime import datetime

from dateutil.tz import tzlocal
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **opts):
        from kompassi.core.models import Event, Organization, Venue
        from kompassi.zombies.enrollment.models import EnrollmentEventMeta

        tz = tzlocal()
        organization = Organization.objects.get(slug="tracon-ry")
        venue, unused = Venue.objects.get_or_create(
            name="Ilmoitetaan myöhemmin",
            defaults=dict(
                name_inessive="Ilmoitetaan myöhemmin",
            ),
        )
        event, unused = Event.objects.get_or_create(
            slug="traconjvk2022",
            defaults=dict(
                public=False,
                name="Traconin JV-kertauskurssi 2022",
                name_genitive="Traconin JV-kertauskurssin",
                name_illative="Traconin JV-kertauskurssille",
                name_inessive="Traconin JV-kertauskurssilla",
                homepage_url="http://ry.tracon.fi/",
                organization=organization,
                start_time=datetime(2022, 8, 14, 8, 0, tzinfo=tz),
                end_time=datetime(2022, 8, 14, 16, 0, tzinfo=tz),
                venue=venue,
            ),
        )

        (admin_group,) = EnrollmentEventMeta.get_or_create_groups(event, ["admins"])

        EnrollmentEventMeta.objects.get_or_create(
            event=event,
            defaults=dict(
                admin_group=admin_group,
                form_class_path="events.traconjvk2022.forms:EnrollmentForm",
                is_participant_list_public=False,
                is_official_name_required=True,
                override_enrollment_form_message="Olethan yhteydessä turva [at] tracon.fi ennen ilmoittautumista, jos olet estynyt pääsemästä yllämainittuihin tapahtumiin ja  haluat neuvotella mahdollisuudesta suorittaa työpanoksen muissa Tracon ry:n tapahtumissa.",
                enrollment_opens=datetime(2022, 7, 6, 8, 0, tzinfo=tz),
                enrollment_closes=datetime(2022, 8, 13, 20, 0, tzinfo=tz),
            ),
        )
