from datetime import date

from django.conf import settings
from django.core.management.base import BaseCommand

from access.models import EmailAliasDomain, EmailAliasType, AccessOrganizationMeta, SMTPServer
from core.models import Organization
from membership.models import MembershipOrganizationMeta, Term
from payments.models import META_DEFAULTS


class Setup:
    def __init__(self):
        pass

    def setup(self):
        self.setup_core()
        #        self.setup_membership()
        self.setup_access()
        self.setup_directory()

    def setup_core(self):
        self.organization, unused = Organization.objects.get_or_create(
            slug="kotae-ry",
            defaults=dict(
                name="Kotae ry",
                homepage_url="https://kotae.fi",
                description="""
Yhdistyksemme tarkoituksena on lisätä, kehittää ja ylläpitää mahdollisuuksia japanilaisen populaarikulttuurin harrastamiseen, erityisesti tapahtumajärjestämisen keinoin. Kotae Ry on voittoa tavoittelematon yhdistys.
                """.strip(),
            ),
        )

        # v10
        self.organization.muncipality = "Tampere"
        self.organization.public = True
        self.organization.save()

    def setup_access(self):
        (admin_group,) = AccessOrganizationMeta.get_or_create_groups(self.organization, ["admins"])

        meta, created = AccessOrganizationMeta.objects.get_or_create(
            organization=self.organization,
            defaults=dict(
                admin_group=admin_group,
            ),
        )

        domain, created = EmailAliasDomain.objects.get_or_create(
            domain_name="kotae.fi",
            defaults=dict(
                organization=self.organization,
            ),
        )

        for type_code, type_metavar in [
            ("access.email_aliases:firstname_surname", "etunimi.sukunimi"),
            ("organizations.kotae_ry.email_aliases:nick", "nick"),
        ]:
            alias_type, created = EmailAliasType.objects.get_or_create(
                domain=domain,
                metavar=type_metavar,
                defaults=dict(
                    account_name_code=type_code,
                ),
            )

        # v14
        EmailAliasType.objects.filter(
            domain=domain,
            metavar="nick",
            priority=0,
        ).update(
            priority=-10,
        )

        internals_domain, created = EmailAliasDomain.objects.get_or_create(
            domain_name="kompassi.eu",
            defaults=dict(
                organization=self.organization,
                has_internal_aliases=True,
            ),
        )

        if settings.DEBUG:
            smtp_server, created = SMTPServer.objects.get_or_create(
                hostname="sakataki.ext.b2.fi",
                ssh_server="neula.kompassi.eu",
                ssh_username="japsu",
                password_file_path_on_server="/home/japsu/smtppasswd",
                trigger_file_path_on_server="/home/japsu/000trigger",
            )

            if created:
                smtp_server.domains.add(domain)

    def setup_directory(self):
        from directory.models import DirectoryOrganizationMeta

        DirectoryOrganizationMeta.objects.get_or_create(organization=self.organization)


class Command(BaseCommand):
    args = ""
    help = "Setup Kotae ry specific stuff"

    def handle(self, *args, **opts):
        Setup().setup()
