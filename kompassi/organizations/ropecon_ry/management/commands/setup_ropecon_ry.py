from django.core.management.base import BaseCommand

from kompassi.access.models import AccessOrganizationMeta, EmailAliasDomain, EmailAliasType
from kompassi.access.models.email_alias_type import EmailAliasVariant
from kompassi.core.models import Organization
from kompassi.involvement.models import Registry
from kompassi.payments.models.payments_organization_meta import META_DEFAULTS, PaymentsOrganizationMeta


class Setup:
    def __init__(self):
        pass

    def setup(self):
        self.setup_core()
        self.setup_payments()
        self.setup_access()
        self.setup_involvement()

    def setup_core(self):
        self.organization, unused = Organization.objects.get_or_create(
            slug="ropecon-ry",
            defaults=dict(
                name="Ropecon ry",
                homepage_url="https://ry.ropecon.fi",
            ),
        )

    def setup_payments(self):
        PaymentsOrganizationMeta.objects.get_or_create(
            organization=self.organization,
            defaults=META_DEFAULTS,
        )

    def setup_access(self):
        (admin_group,) = AccessOrganizationMeta.get_or_create_groups(self.organization, ["admins"])

        AccessOrganizationMeta.objects.get_or_create(
            organization=self.organization,
            defaults=dict(
                admin_group=admin_group,
            ),
        )

        domain, _ = EmailAliasDomain.objects.get_or_create(
            domain_name="ropecon.fi",
            defaults=dict(
                organization=self.organization,
            ),
        )

        for variant in [
            EmailAliasVariant.FIRSTNAME_LASTNAME,
            EmailAliasVariant.NICK,
        ]:
            EmailAliasType.objects.get_or_create(
                domain=domain,
                variant_slug=variant.name,
            )

    def setup_involvement(self):
        Registry.objects.get_or_create(
            scope=self.organization.scope,
            slug="volunteers",
            defaults=dict(
                title_en="Volunteers of Ropecon ry",
                title_fi="Ropecon ry:n vapaaehtoisrekisteri",
            ),
        )


class Command(BaseCommand):
    args = ""
    help = "Setup Ropecon ry specific stuff"

    def handle(self, *args, **opts):
        Setup().setup()
