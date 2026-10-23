from datetime import timedelta

from django.core.management.base import BaseCommand

from kompassi.core.models import Organization
from kompassi.involvement.models.registry import Registry
from kompassi.payments.models import PaymentsOrganizationMeta
from kompassi.payments.models.payments_organization_meta import META_DEFAULTS


class Setup:
    def __init__(self):
        pass

    def setup(self):
        self.setup_core()
        self.setup_payments()
        self.setup_involvement()

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

    def setup_involvement(self):
        Registry.objects.update_or_create(
            scope=self.organization.scope,
            slug="volunteers",
            defaults=dict(
                title_en="Volunteers of Cosmocon ry",
                title_fi="Cosmocon ry:n vapaaehtoisrekisteri",
                title_sv="Cosmocon ry:s volontärregister",
                policy_url_fi="https://cosmocon.fi/tietosuoja",
                default_retention_period=timedelta(days=2 * 365),
            ),
        )


class Command(BaseCommand):
    args = ""
    help = "Setup Cosmocon ry specific stuff"

    def handle(self, *args, **opts):
        Setup().setup()
