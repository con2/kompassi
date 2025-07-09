from datetime import datetime

from django.core.management.base import BaseCommand
from django.utils.timezone import get_current_timezone

from core.models import Event, Organization, Venue
from involvement.models.registry import Registry
from program_v2.models.meta import ProgramV2EventMeta


class Command(BaseCommand):
    def handle(self, *args, **options):
        tz = get_current_timezone()

        venue, unused = Venue.objects.get_or_create(
            name="Alandica Kultur och Kongress (Mariehamn)",
            defaults=dict(
                name_inessive="Alandicassa",
            ),
        )

        organization, unused = Organization.objects.get_or_create(
            slug="maa-ja-ilma-ry",
            defaults=dict(
                name="Maa ja ilma ry",
            ),
        )

        event, unused = Event.objects.update_or_create(
            slug="archipelacon2025",
            defaults=dict(
                name="Archipelacon 2 (2025)",
                name_genitive="Archipelaconin",
                name_illative="Archipelaconiin",
                name_inessive="Archipelaconissa",
                homepage_url="https://archipelacon.org/",
                organization=organization,
                start_time=datetime(2025, 6, 26, 11, 0, tzinfo=tz),
                end_time=datetime(2025, 6, 29, 18, 8, tzinfo=tz),
                venue=venue,
            ),
        )

        # TODO(Archipelacon): Define your volunteer registry
        registry, _created = Registry.objects.get_or_create(
            scope=organization.scope,
            slug="volunteers",
            defaults=dict(
                title_fi="Archipelaconin vapaaehtoisrekisteri",
                title_en="Volunteers of Archipelacon",
            ),
        )

        (admin_group,) = ProgramV2EventMeta.get_or_create_groups(event, ["admins"])
        ProgramV2EventMeta.objects.update_or_create(
            event=event,
            defaults=dict(
                admin_group=admin_group,
                contact_email="Archipelacon programme team <programme@archipelacon.org>",
                default_registry=registry,
            ),
        )

        # ProgramOfferWorkflow.backfill(event)
