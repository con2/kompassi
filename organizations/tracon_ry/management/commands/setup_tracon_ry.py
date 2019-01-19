# encoding: utf-8

from datetime import date, datetime, timedelta

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.timezone import now

from dateutil.tz import tzlocal

from access.models import EmailAliasDomain, EmailAliasType, AccessOrganizationMeta, SMTPServer
from core.models import Organization
from core.utils import slugify
from membership.models import MembershipOrganizationMeta, Term


class Setup(object):
    def __init__(self):
        pass

    def setup(self):
        self.setup_core()
        self.setup_membership()
        self.setup_access()
        self.setup_directory()

    def setup_core(self):
        self.organization, unused = Organization.objects.get_or_create(
            slug='tracon-ry',
            defaults=dict(
                name='Tracon ry',
                homepage_url='https://ry.tracon.fi',
                logo_url='https://media.tracon.fi/ry/vaakuna-vari.png',
                description="""
Tracon ry on tamperelainen yhdistys, jonka tarkoituksena on edistää, kehittää ja tehdä tunnetuksi roolipeli-, korttipeli-, lautapeli-, miniatyyripeli-, animaatio-, elokuva- ja sarjakuvaharrastuksia, sekä näihin liittyviä alakulttuureita.

Yhdistyksen keskeisintä toimintaa on roolipeli- ja animetapahtuma Traconin järjestäminen. Yhdistyksen jäseniä ovat tapahtuman järjestämiseen osallistuvat aktiivit.

Yhdistys toimii läheisessä yhteistyössä muiden tamperelaisten alan kerhojen kanssa. Näitä ovat muun muassa Anime- ja mangayhteisö Hidoi ry, Tampereen teekkareiden roolipelikerho Excalibur, Tampereen Seudun Roolipelaajat ry, Herwannan Nykyaikain Teekkarein Animaatioiltamat, Eru, Tampereen yliopiston roolipelaajat ja Roolipeliseura Korpimetsä.

Tracon ry:n yhdistysrekisteritunnus on 194.820.
                """.strip(),
            )
        )

        # v10
        self.organization.muncipality = 'Tampere'
        self.organization.public = True
        self.organization.save()

    def setup_membership(self):
        membership_admin_group, = MembershipOrganizationMeta.get_or_create_groups(self.organization, ['admins'])
        members_group, = MembershipOrganizationMeta.get_or_create_groups(self.organization, ['members'])

        self.meta, created = MembershipOrganizationMeta.objects.get_or_create(organization=self.organization, defaults=dict(
            admin_group=membership_admin_group,
            members_group=members_group,
            receiving_applications=True,
            membership_requirements="""
Yhdistyksen varsinaiseksi jäseneksi voi liittyä jokainen yksityinen henkilö tai oikeuskelpoinen yhdistys, joka hyväksyy yhdistyksen tarkoituksen ja säännöt ja osallistuu sen toimintaan.

Jäsenhakemukset hyväksyy yhdistyksen hallitus, jolla on oikeus olla hyväksymättä hakemusta, mikäli siihen on selvät perusteet.
""".strip(),
        ))

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
                )
            )

    def setup_access(self):
        admin_group, = AccessOrganizationMeta.get_or_create_groups(self.organization, ['admins'])

        meta, created = AccessOrganizationMeta.objects.get_or_create(
            organization=self.organization,
            defaults=dict(
                admin_group=admin_group,
            )
        )

        domain, created = EmailAliasDomain.objects.get_or_create(
            domain_name='tracon.fi',
            defaults=dict(
                organization=self.organization,
            )
        )

        for type_code, type_metavar in [
            ('access.email_aliases:firstname_surname', 'etunimi.sukunimi'),
            ('events.tracon11.email_aliases:requested_alias_or_nick', 'nick'),
        ]:
            alias_type, created = EmailAliasType.objects.get_or_create(
                domain=domain,
                account_name_code=type_code,
                defaults=dict(
                    metavar=type_metavar,
                )
            )

        # v14
        EmailAliasType.objects.filter(
            domain=domain,
            metavar='nick',
            priority=0,
        ).update(
            priority=-10,
        )

        internals_domain, created = EmailAliasDomain.objects.get_or_create(
            domain_name='kompassi.eu',
            defaults=dict(
                organization=self.organization,
                has_internal_aliases=True,
            )
        )

        if settings.DEBUG:
            smtp_server, created = SMTPServer.objects.get_or_create(
                hostname='sakataki.ext.b2.fi',
                ssh_server='neula.kompassi.eu',
                ssh_username='japsu',
                password_file_path_on_server='/home/japsu/smtppasswd',
                trigger_file_path_on_server='/home/japsu/000trigger',
            )

            if created:
                smtp_server.domains.add(domain)

    def setup_directory(self):
        from directory.models import DirectoryOrganizationMeta

        DirectoryOrganizationMeta.objects.get_or_create(organization=self.organization)


class Command(BaseCommand):
    args = ''
    help = 'Setup Tracon ry specific stuff'

    def handle(self, *args, **opts):
        Setup().setup()
