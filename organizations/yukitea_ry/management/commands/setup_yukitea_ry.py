# encoding: utf-8

from datetime import date, datetime, timedelta

from django.core.management.base import BaseCommand
from django.utils.timezone import now

from dateutil.tz import tzlocal

from access.models import EmailAliasDomain, EmailAliasType, AccessOrganizationMeta
from core.models import Organization
from core.utils import slugify
from membership.models import MembershipOrganizationMeta, Term


class Setup(object):
    def __init__(self):
        pass

    def setup(self):
        self.setup_core()
        self.setup_membership()

    def setup_core(self):
        self.organization, unused = Organization.objects.get_or_create(
            slug='yukitea-ry',
            defaults=dict(
                name='Yukitea ry',
                homepage_url='http://www.yukicon.fi',
                logo_url='',
                description=u"""
Yukitea ry on voittoa tavoittelematon yhdistys, jonka tavoite on edistää ja kehittää videopeli-, animaatio-, elokuva- ja sarjakuvaharrastuksia.

Yukitea ry on vuosittaisen Yukicon -anime- ja pelitapahtuman järjestäjä.
                """.strip(),
            )
        )

        # v10
        self.organization.muncipality = u'Espoo'
        self.organization.public = True
        self.organization.save()

    def setup_membership(self):
        membership_admin_group, = MembershipOrganizationMeta.get_or_create_groups(self.organization, ['admins'])
        members_group, = MembershipOrganizationMeta.get_or_create_groups(self.organization, ['members'])

        self.meta, created = MembershipOrganizationMeta.objects.get_or_create(organization=self.organization, defaults=dict(
            admin_group=membership_admin_group,
            members_group=members_group,
            receiving_applications=False,
            membership_requirements=u"""
Yukitea ry hyväksyy varsinaisia ja kannatusjäseniä. Kompassin kautta on mahdollista liittyä vain kannatusjäseneksi. Kannatusjäsen on jäsen, joka tukee yhdistyksen toimintaa rahallisesti osallistumatta siihen aktiivisesti. Kannatusjäsenillä ei ole läsnäolo-, puhe- tai äänioikeutta yhdistyksen kokouksissa.

Yhdistyksen varsinaisiksi jäseniksi voidaan hyväksyä henkilöitä, jotka osallistuvat yhdistyksen toimintaan. Jos haluat liittyä yhdistyksen varsinaiseksi jäseneksi, ota yhteyttä yhdistyksen hallitukseen yukicon@yukicon.fi.
""".strip(),
        ))

        for year, membership_fee_cents in [
            (2016, 5000),
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


class Command(BaseCommand):
    args = ''
    help = 'Setup Yukitea ry specific stuff'

    def handle(self, *args, **opts):
        Setup().setup()
