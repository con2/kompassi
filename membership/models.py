# encoding: utf-8

from datetime import date

from django.conf import settings
from django.contrib.auth.models import Group
from django.db import models

from core.models import Organization, Person, GroupManagementMixin
from core.utils import format_date, ensure_user_group_membership
from tickets.utils import format_price


class MembershipOrganizationMeta(models.Model, GroupManagementMixin):
    organization = models.OneToOneField(Organization, primary_key=True, verbose_name=u'Organisaatio')
    admin_group = models.ForeignKey(Group, verbose_name=u'Ylläpitäjäryhmä', related_name='admin_group_for')
    members_group = models.ForeignKey(Group, verbose_name=u'Jäsenryhmä', related_name='members_group_for')
    receiving_applications = models.BooleanField(
        default=True,
        verbose_name=u'Ottaa vastaan hakemuksia',
        help_text=u'Tämä asetus kontrolloi, voiko yhdistyksen jäseneksi hakea suoraan Kompassin kautta.',
    )
    membership_requirements = models.TextField(
        blank=True,
        verbose_name=u'Kuka voi hakea jäsenyyttä?',
        help_text=u'Esim. copy-paste säännöistä.'
    )

    def __unicode__(self):
        return self.organization.name if self.organization is not None else u'None'

    class Meta:
        verbose_name = u'Jäsenrekisterin asetukset'
        verbose_name = u'Jäsenrekisterien asetukset'

    def get_group(self, suffix):
        group_name = self.make_group_name(self.organization, suffix)

        return Group.objects.get(name=group_name)

    def get_current_term(self, d=None):
        if d is None:
            d = date.today()

        return self.organization.terms.get(
            start_date__lte=d,
            end_date__gte=d,
        )


STATE_CHOICES = [
    (u'approval', u'Odottaa hyväksyntää'),
    (u'in_effect', u'Voimassa'),
    (u'discharged', u'Erotettu'),
]

STATE_CSS = dict(
    approval='label-info',
    in_effect='label-success',
    discharged='label-danger',
)


class Membership(models.Model):
    organization = models.ForeignKey(Organization, verbose_name=u'Yhdistys', related_name='memberships')
    person = models.ForeignKey(Person, verbose_name=u'Henkilö', related_name='memberships')
    state = models.CharField(
        max_length=max(len(key) for (key, val) in STATE_CHOICES),
        choices=STATE_CHOICES,
        verbose_name=u'Tila',
    )
    message = models.TextField(
        blank=True,
        verbose_name=u'Viesti hakemuksen käsittelijälle',
    )

    @property
    def is_pending_approval(self):
        return self.state == 'approval'

    @property
    def is_in_effect(self):
        return self.state == 'in_effect'

    @property
    def is_discharged(self):
        return self.state == 'discharged'

    @property
    def formatted_state(self):
        return self.get_state_display()

    @property
    def state_css(self):
        return STATE_CSS[self.state]

    @property
    def events(self):
        # XXX STUB
        return []

    def to_html_print(self):
        return u'{surname}, {official_first_names}, {muncipality}'.format(
            surname=self.person.surname,
            official_first_names=self.person.official_first_names,
            muncipality=self.person.muncipality,
        )

    def __unicode__(self):
        return u"{organization}/{person}".format(
            organization=self.organization.name if self.organization else None,
            person=self.person.official_name if self.person else None,
        )

    @classmethod
    def get_csv_fields(cls, unused_organization):
        return [
            (Person, 'surname'),
            (Person, 'official_first_names_or_first_name'),
            (Person, 'muncipality'),
            (Person, 'email'),
            (Person, 'phone'),
            (Person, 'birth_date'),
            (cls, 'formatted_state'),
        ]

    def get_csv_related(self):
        return {
            Membership: self,
            Person: self.person,
        }

    def get_previous_and_next(self):
        if not self.pk:
            return None, None

        # TODO inefficient, done using a list
        memberships = list(self.organization.memberships.order_by('person__surname', 'person__official_first_names', 'id'))

        previous_membership = None
        current_membership = None

        for next_signup in memberships + [None]:
            if current_membership and current_membership.pk == self.pk:
                return previous_membership, next_signup

            previous_membership = current_membership
            current_membership = next_signup

        return None, None

    def apply_state(self):
        if 'background_tasks' in settings.INSTALLED_APPS:
            from .tasks import membership_apply_state
            membership_apply_state.delay(self.pk)
        else:
            self._apply_state()

    def _apply_state(self):
        self._apply_state_group_membership()
        self._apply_state_email_aliases()

    def _apply_state_group_membership(self):
        if self.person.user:
            members_group = self.organization.membership_organization_meta.members_group

            if self.is_in_effect:
                groups_to_add = [members_group]
                groups_to_remove = []
            else:
                groups_to_add = []
                groups_to_remove = [members_group]

            ensure_user_group_membership(self.person.user, groups_to_add, groups_to_remove)

    def _apply_state_email_aliases(self):
        if 'access' not in settings.INSTALLED_APPS:
            return

        from access.models import GroupEmailAliasGrant
        GroupEmailAliasGrant.ensure_aliases(self.person)

    class Meta:
        verbose_name = u'Jäsenyys'
        verbose_name_plural = u'Jäsenyydet'


class Term(models.Model):
    organization = models.ForeignKey(Organization,
        verbose_name=u'Yhdistys',
        related_name='terms'
    )
    title = models.CharField(max_length=63, verbose_name=u'Otsikko', help_text=u'Yleensä vuosiluku')
    start_date = models.DateField(verbose_name=u'Alkamispäivä', help_text=u'Yleensä vuoden ensimmäinen päivä')
    end_date = models.DateField(verbose_name=u'Päättymispäivä', help_text=u'Yleensä vuoden viimeinen päivä')

    entrance_fee_cents = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True,
        verbose_name=u'Liittymismaksu (snt)',
        help_text=u'Arvo 0 (nolla senttiä) tarkoittaa, että yhdistyksellä ei ole tällä kaudella liittymismaksua. '
            u'Arvon puuttuminen tarkoittaa, että liittymismaksu ei ole tiedossa.',
    )

    membership_fee_cents = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True,
        verbose_name=u'Jäsenmaksu (snt)',
        help_text=u'Arvo 0 (nolla senttiä) tarkoittaa, että yhdistyksellä ei ole tällä kaudella jäsenmaksua. '
            u'Arvon puuttuminen tarkoittaa, että liittymismaksu ei ole tiedossa.',
    )

    @property
    def formatted_entrance_fee(self):
        if self.entrance_fee_cents is None:
            return u'Liittymismaksu ei ole tiedossa.'
        elif self.entrance_fee_cents == 0:
            return u'Ei liittymismaksua.'
        else:
            return format_price(self.entrance_fee_cents)

    @property
    def formatted_membership_fee(self):
        if self.membership_fee_cents is None:
            return u'Jäsenmaksu ei ole tiedossa.'
        elif self.membership_fee_cents == 0:
            return u'Ei jäsenmaksua kaudella {title}.'.format(title=self.title,)
        else:
            return u'{money} (voimassa {end_date} asti).'.format(
                money=format_price(self.membership_fee_cents),
                end_date=format_date(self.end_date),
            )
    def save(self, *args, **kwargs):
        if self.start_date and not self.title:
            self.title = unicode(self.start_date.year)

        return super(Term, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = u'Toimikausi'
        verbose_name_plural = u'Toimikaudet'


class MembershipFeePayment(models.Model):
    term = models.ForeignKey(Term, related_name='membership_fee_payments')
    member = models.ForeignKey(Membership, related_name='membership_fee_payments')

    payment_date = models.DateField(auto_now_add=True)

    def __unicode__(self):
        return self.term.title if self.term else u'None'

    class Meta:
        verbose_name = u'Jäsenmaksusuoritus'
        verbose_name_plural = u'Jäsenmaksusuoritukset'

    def admin_get_organization(self):
        return self.term.organization if self.term else None
    admin_get_organization.short_description = u'Yhdistys'
    admin_get_organization.admin_order_field = 'organization'

    def admin_get_official_name(self):
        return self.member.person.official_name if self.member else None
    admin_get_official_name.short_description = u'Jäsen'
    admin_get_official_name.admin_order_field = u'member'
