# encoding: utf-8

from django.contrib.auth.models import Group
from django.db import models

from core.models import Organization, Person, GroupManagementMixin


class MembershipOrganizationMeta(models.Model, GroupManagementMixin):
    organization = models.OneToOneField(Organization, primary_key=True, verbose_name=u'Organisaatio')
    admin_group = models.ForeignKey(Group, verbose_name=u'Ylläpitäjäryhmä')
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
    membership_fee = models.TextField(
        blank=True,
        verbose_name=u'Jäsenmaksu',
        help_text=u'Minkä suuruinen on liittymis- ja jäsenmaksu ja miten se maksetaan?',
    )

    def __unicode__(self):
        return self.organization.name if self.organization is not None else u'None'

    class Meta:
        verbose_name = u'Jäsenrekisterin asetukset'
        verbose_name = u'Jäsenrekisterien asetukset'

    def get_group(self, suffix):
        group_name = self.make_group_name(self.organization, suffix)

        return Group.objects.get(name=group_name)


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
    organization = models.ForeignKey(Organization, verbose_name=u'Organisaatio', related_name='members')
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

    def to_html_print(self):
        return u'{surname}, {first_name}, {muncipality}'.format(
            surname=self.person.surname,
            first_name=self.person.first_name,
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
            (Person, 'first_name'),
            (Person, 'muncipality'),
            (cls, 'formatted_state'),
        ]

    def get_csv_related(self):
        return {
            Membership: self,
            Person: self.person,
        }

    class Meta:
        verbose_name = u'Jäsenyys'
        verbose_name_plural = u'Jäsenyydet'
