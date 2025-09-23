from datetime import date

from django.conf import settings
from django.core.management.base import BaseCommand

from kompassi.access.models import AccessOrganizationMeta, EmailAliasDomain, EmailAliasType, SMTPServer
from kompassi.access.models.email_alias_type import EmailAliasVariant
from kompassi.core.models import Organization
from kompassi.involvement.models.registry import Registry
from kompassi.membership.models import MembershipOrganizationMeta, Term
from kompassi.payments.models import PaymentsOrganizationMeta
from kompassi.payments.models.payments_organization_meta import META_DEFAULTS


class Setup:
    def __init__(self):
        pass

    def setup(self):
        self.setup_core()
        self.setup_membership()
        self.setup_access()
        self.setup_payments()
        self.setup_involvement()

    def setup_core(self):
        self.organization, unused = Organization.objects.get_or_create(
            slug="tracon-ry",
            defaults=dict(
                name="Tracon ry",
                homepage_url="https://ry.tracon.fi",
                logo_url="https://media.tracon.fi/ry/vaakuna-vari.png",
                description="""
Tracon ry on tamperelainen yhdistys, jonka tarkoituksena on edistää, kehittää ja tehdä tunnetuksi roolipeli-, korttipeli-, lautapeli-, miniatyyripeli-, animaatio-, elokuva- ja sarjakuvaharrastuksia, sekä näihin liittyviä alakulttuureita.

Yhdistyksen keskeisintä toimintaa on roolipeli- ja animetapahtuma Traconin järjestäminen. Yhdistyksen jäseniä ovat tapahtuman järjestämiseen osallistuvat aktiivit.

Yhdistys toimii läheisessä yhteistyössä muiden tamperelaisten alan kerhojen kanssa. Näitä ovat muun muassa Anime- ja mangayhteisö Hidoi ry, Tampereen teekkareiden roolipelikerho Excalibur, Tampereen Seudun Roolipelaajat ry, Herwannan Nykyaikain Teekkarein Animaatioiltamat, Eru, Tampereen yliopiston roolipelaajat ja Roolipeliseura Korpimetsä.

Tracon ry:n yhdistysrekisteritunnus on 194.820.
                """.strip(),
                panel_css_class="panel-danger",
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
Yhdistyksen varsinaiseksi jäseneksi voi liittyä jokainen yksityinen henkilö tai oikeuskelpoinen yhdistys, joka hyväksyy yhdistyksen tarkoituksen ja säännöt ja osallistuu sen toimintaan.

Jäsenhakemukset hyväksyy yhdistyksen hallitus, jolla on oikeus olla hyväksymättä hakemusta, mikäli siihen on selvät perusteet.
""".strip(),
            ),
        )

        for year, membership_fee_cents in [
            (2015, 100),
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
            domain_name="tracon.fi",
            defaults=dict(
                organization=self.organization,
            ),
        )

        for variant in [
            EmailAliasVariant.FIRSTNAME_LASTNAME,
            EmailAliasVariant.CUSTOM,
        ]:
            EmailAliasType.objects.get_or_create(
                domain=domain,
                variant_slug=variant.name,
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

    def setup_payments(self):
        PaymentsOrganizationMeta.objects.get_or_create(
            organization=self.organization,
            defaults=META_DEFAULTS,
        )

    def setup_involvement(self):
        volunteers, _ = Registry.objects.get_or_create(
            scope=self.organization.scope,
            slug="volunteers",
            defaults=dict(
                title_en="Volunteers of Tracon ry",
                title_fi="Tracon ry:n vapaaehtoisrekisteri",
            ),
        )


class Command(BaseCommand):
    args = ""
    help = "Setup Tracon ry specific stuff"

    def handle(self, *args, **opts):
        Setup().setup()
