from datetime import date

from django.conf import settings
from django.core.management.base import BaseCommand

from access.models import AccessOrganizationMeta, EmailAliasDomain, EmailAliasType, SMTPServer
from core.models import Organization
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
            slug="kotae-ry",
            defaults=dict(
                name="Kotae ry",
                homepage_url="https://kotae.fi",
                description="""
Kotae ry:n tarkoituksena on lisätä, kehittää ja ylläpitää mahdollisuuksia japanilaisen populaarikulttuurin harrastamiseen, erityisesti tapahtumajärjestämisen keinoin. Kotae Ry on voittoa tavoittelematon yhdistys. Yhdistyksen keskeisenä toimintana on Tampereella pidettävän japanilaisen ja korealaisen populaarikulttuurin tapahtuman, Kotae Expon, järjestäminen.

Kotae ry:n varsinainen jäsenyys kaudella 1.10.2023-30.9.2024 on maksuton. Varsinainen jäsen voi halutessaan maksaa vapaaehtoisen 10 euron jäsenmaksun. Ilmoitathan hakemuksessasi mikäli olet kiinnostunut vapaaehtoisesta jäsenmaksusta. Toimitamme laskun erikseen sähköpostitse kiinnostuksensa ilmaisseille hyväksytyille jäsenille.

Kotae ry:hyn voi liittyä myös kannattajajäsenenä. Kannattajajäsenmaksu kaudella 1.10.2023-30.9.2024 on 50 euroa. Ilmoitathan hakemuksessasi mikäli olet kiinnostunut kannattajajäsenyydestä. Toimitamme laskun erikseen sähköpostitse kiinnostuksensa ilmaisseille hyväksytyille kannattajajäsenille.

Kotae ry:n Y-tunnus on 3364741-7.
                """.strip(),
            ),
        )

        # v10
        self.organization.muncipality = "Tampere"
        self.organization.public = True
        self.organization.save()

    def setup_membership(self):
        (membership_admin_group,) = MembershipOrganizationMeta.get_or_create_groups(self.organization, ["admins"])
        (members_group,) = MembershipOrganizationMeta.get_or_create_groups(self.organization, ["members"])

        self.meta, created = MembershipOrganizationMeta.objects.get_or_create(
            organization=self.organization,
            defaults=dict(
                admin_group=membership_admin_group,
                members_group=members_group,
                receiving_applications=True,
                membership_requirements="""
Yhdistyksen varsinaiseksi jäseneksi voi päästä luonnollinen henkilö tai oikeuskelpoinen yhdistys, joka hyväksyy yhdistyksen tarkoituksen, toiminnan ja yleiset periaatteet, ja jonka yhdistyksen hallitus hyväksyy jäseneksi. Yhdistyksen hallituksella on oikeus olla hyväksymättä jäsenhakemusta, mikäli siihen on selvät perusteet.
""".strip(),
            ),
        )

        for year_1, year_2, membership_fee_cents in [
            (2023, 2024, 0),
        ]:
            start_date = date(year_1, 10, 1)
            end_date = date(year_2, 9, 30)

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


class Command(BaseCommand):
    args = ""
    help = "Setup Kotae ry specific stuff"

    def handle(self, *args, **opts):
        Setup().setup()
