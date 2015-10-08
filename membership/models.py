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

    def __unicode__(self):
        return self.organization.name if self.organization is not None else u'None'

    class Meta:
        verbose_name = u'Jäsenrekisterin asetukset'
        verbose_name = u'Jäsenrekisterien asetukset'

    def get_group(self, suffix):
        group_name = self.make_group_name(self.organization, suffix)

        return Group.objects.get(name=group_name)


class Membership(models.Model):
    organization = models.ForeignKey(Organization, verbose_name=u'Organisaatio')
    person = models.ForeignKey(Person, verbose_name=u'Henkilö')

    def __unicode__(self):
        return u"{organization}/{person}".format(
            organization=self.organization,
            person=self.person,
        )

    class Meta:
        verbose_name = u'Jäsenyys'
        verbose_name_plural = u'Jäsenyydet'
