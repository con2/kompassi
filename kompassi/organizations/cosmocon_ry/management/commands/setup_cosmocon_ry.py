from django.core.management.base import BaseCommand

from kompassi.core.models import Organization
from kompassi.payments.models import PaymentsOrganizationMeta
from kompassi.payments.models.payments_organization_meta import META_DEFAULTS


class Setup:
    def __init__(self):
        pass

    def setup(self):
        self.setup_core()
        self.setup_payments()

    def setup_core(self):
        self.organization, _ = Organization.objects.get_or_create(
            slug="cosmocon-ry",
            defaults=dict(
                name="Cosmocon ry",
                homepage_url="https://cosmocon.fi",
                logo_url="https://cosmocon.fi/wp-content/uploads/2024/10/Logo_2400px_vihrea.png",
            ),
        )
        self.organization.full_clean()

    def setup_payments(self):
        PaymentsOrganizationMeta.objects.get_or_create(
            organization=self.organization,
            defaults=META_DEFAULTS,
        )


class Command(BaseCommand):
    args = ""
    help = "Setup Cosmocon ry specific stuff"

    def handle(self, *args, **opts):
        Setup().setup()
