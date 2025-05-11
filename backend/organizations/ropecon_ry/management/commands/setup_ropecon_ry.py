from django.core.management.base import BaseCommand

from access.models import AccessOrganizationMeta, EmailAliasDomain, EmailAliasType
from core.models import Organization
from involvement.models import Registry
from payments.models.payments_organization_meta import META_DEFAULTS, PaymentsOrganizationMeta


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

        for priority, (type_code, type_metavar) in enumerate(
            [
                ("access.email_aliases:firstname_surname", "firstname.lastname"),
                ("access.email_aliases:nick", "nick"),
            ]
        ):
            EmailAliasType.objects.get_or_create(
                domain=domain,
                metavar=type_metavar,
                defaults=dict(
                    account_name_code=type_code,
                    priority=priority,
                ),
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
