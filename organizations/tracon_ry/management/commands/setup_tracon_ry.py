# encoding: utf-8

from datetime import datetime, timedelta

from django.core.management.base import BaseCommand, make_option
from django.utils.timezone import now

from dateutil.tz import tzlocal

from core.utils import slugify


class Setup(object):
    def __init__(self):
        pass

    def setup(self):
        self.setup_core()
        self.setup_membership()

    def setup_core(self):
        from core.models import Organization

        self.organization, unused = Organization.objects.get_or_create(
            slug='tracon-ry',
            defaults=dict(
                name='Tracon ry',
                homepage_url='https://ry.tracon.fi',
                logo_url='https://media.tracon.fi/ry/vaakuna-vari.png',
                receiving_applications=False,
                description=u"""
Tracon ry on tamperelainen yhdistys, jonka tarkoituksena on edistää, kehittää ja tehdä tunnetuksi roolipeli-, korttipeli-, lautapeli-, miniatyyripeli-, animaatio-, elokuva- ja sarjakuvaharrastuksia, sekä näihin liittyviä alakulttuureita.

Yhdistyksen keskeisintä toimintaa on roolipeli- ja animetapahtuma Traconin järjestäminen. Yhdistyksen jäseniä ovat tapahtuman järjestämiseen osallistuvat aktiivit.

Yhdistys toimii läheisessä yhteistyössä muiden tamperelaisten alan kerhojen kanssa. Näitä ovat muun muassa Anime- ja mangayhteisö Hidoi ry, Tampereen teekkareiden roolipelikerho Excalibur, Tampereen Seudun Roolipelaajat ry, Herwannan Nykyaikain Teekkarein Animaatioiltamat, Eru, Tampereen yliopiston roolipelaajat ja Roolipeliseura Korpimetsä.

Tracon ry:n yhdistysrekisteritunnus on 194.820.
                """.strip(),
            )
        )

    def setup_membership(self):
        from membership.models import MembershipOrganizationMeta

        membership_admin_group, created = MembershipOrganizationMeta.get_or_create_group(self.organization, 'admins')

        self.meta = MembershipOrganizationMeta.objects.get_or_create(organization=self.organization, defaults=dict(
            admin_group=membership_admin_group
        ))


class Command(BaseCommand):
    args = ''
    help = 'Setup Tracon ry specific stuff'

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
