# encoding: utf-8

from datetime import date, datetime, timedelta

from django.core.management.base import BaseCommand, make_option
from django.utils.timezone import now

from dateutil.tz import tzlocal

from access.models import EmailAliasDomain, EmailAliasType
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

    def setup_core(self):
        self.organization, unused = Organization.objects.get_or_create(
            slug='aicon-ry',
            defaults=dict(
                name='Aicon ry',
                homepage_url='https://aicon.fi',
            )
        )

        # v10
        self.organization.muncipality = u'Tampere'
        self.organization.public = True
        self.organization.save()

    def setup_membership(self):
        membership_admin_group, created = MembershipOrganizationMeta.get_or_create_group(self.organization, 'admins')

        self.meta, created = MembershipOrganizationMeta.objects.get_or_create(organization=self.organization, defaults=dict(
            admin_group=membership_admin_group,
        ))

        for year, membership_fee_cents in [
            (2015, 500),
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
        domain, created = EmailAliasDomain.objects.get_or_create(
            domain_name='aicon.fi',
            defaults=dict(
                organization=self.organization,
            )
        )

        for type_code, type_metavar in [
            ('access.email_aliases:firstname_surname', u'etunimi.sukunimi'),
            ('access.email_aliases:nick', u'nick'),
        ]:
            alias_type, created = EmailAliasType.objects.get_or_create(
                domain=domain,
                account_name_code=type_code,
                defaults=dict(
                    metavar=type_metavar,
                )
            )


class Command(BaseCommand):
    args = ''
    help = 'Setup Aicon ry specific stuff'

    option_list = BaseCommand.option_list + (
        make_option('--test',
            action='store_true',
            dest='test',
            default=False,
            help='Set the organization up for testing',
        ),
    )

    def handle(self, *args, **opts):
        Setup().setup()
