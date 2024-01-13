from django.core.management.base import BaseCommand

from core.models import Organization
from payments.models.payments_organization_meta import META_DEFAULTS


class Setup:
    def __init__(self):
        pass

    def setup(self):
        self.setup_core()
        self.setup_payments()

    def setup_core(self):
        self.organization, unused = Organization.objects.get_or_create(
            slug="ropecon-ry",
            defaults=dict(
                name="Ropecon ry",
                homepage_url="https://ry.ropecon.fi",
            ),
        )

    def setup_payments(self):
        from payments.models import PaymentsOrganizationMeta

        PaymentsOrganizationMeta.objects.get_or_create(
            organization=self.organization,
            defaults=META_DEFAULTS,
        )


class Command(BaseCommand):
    args = ""
    help = "Setup Tracon ry specific stuff"

    def handle(self, *args, **opts):
        Setup().setup()
