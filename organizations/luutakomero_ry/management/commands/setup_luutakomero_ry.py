from datetime import date, datetime, timedelta

from django.core.management.base import BaseCommand
from django.utils.timezone import now

from dateutil.tz import tzlocal

from access.models import EmailAliasDomain, EmailAliasType, AccessOrganizationMeta
from core.models import Organization
from core.utils import slugify
from membership.models import MembershipOrganizationMeta, Term


class Setup:
    def __init__(self):
        pass

    def setup(self):
        self.setup_core()
        self.setup_membership()
        self.setup_access()

    def setup_core(self):
        self.organization, unused = Organization.objects.get_or_create(
            slug="luutakomero-ry",
            defaults=dict(
                name="Luutakomero ry",
                homepage_url="https://www.tylycon.fi",
                # logo_url='https://media.tracon.fi/ry/vaakuna-vari.png',
                description="Luutakomero ry järjestää Harry Potter -fanitapahtuma Tylyconia.",
                muncipality="Helsinki",
                public=True,
            ),
        )

    def setup_membership(self):
        (membership_admin_group,) = MembershipOrganizationMeta.get_or_create_groups(self.organization, ["admins"])
        (members_group,) = MembershipOrganizationMeta.get_or_create_groups(self.organization, ["members"])

        self.meta, created = MembershipOrganizationMeta.objects.get_or_create(
            organization=self.organization,
            defaults=dict(
                admin_group=membership_admin_group,
                members_group=members_group,
                receiving_applications=True,
                membership_requirements="",
            ),
        )

        for year, membership_fee_cents in [
            # (2015, 100),
        ]:
            start_date = date(year, 1, 1)
            end_date = date(year, 12, 31)

            Term.objects.get_or_create(
                organization=self.organization,
                start_date=start_date,
                defaults=dict(
                    end_date=end_date,
                    entrance_fee_cents=0,
                    membership_fee_cents=membership_fee_cents,
                ),
            )

    def setup_access(self):
        (admin_group,) = AccessOrganizationMeta.get_or_create_groups(self.organization, ["admins"])

        meta, created = AccessOrganizationMeta.objects.get_or_create(
            organization=self.organization,
            defaults=dict(
                admin_group=admin_group,
            ),
        )

        domain, created = EmailAliasDomain.objects.get_or_create(
            domain_name="tylycon.fi",
            defaults=dict(
                organization=self.organization,
            ),
        )

        for type_code, type_metavar in [
            ("access.email_aliases:firstname_surname", "etunimi.sukunimi"),
            ("access.email_aliases:nick", "nick"),
        ]:
            alias_type, created = EmailAliasType.objects.get_or_create(
                domain=domain,
                account_name_code=type_code,
                defaults=dict(
                    metavar=type_metavar,
                ),
            )


class Command(BaseCommand):
    args = ""
    help = "Setup Luutakomero ry specific stuff"

    def handle(self, *args, **opts):
        Setup().setup()
