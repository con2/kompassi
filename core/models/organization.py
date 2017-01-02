# encoding: utf-8

import logging

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from ..utils import SLUG_FIELD_PARAMS, slugify, pick_attrs


logger = logging.getLogger('kompassi')


class Organization(models.Model):
    slug = models.CharField(**SLUG_FIELD_PARAMS)

    name = models.CharField(max_length=255, verbose_name=u'Nimi')
    name_genitive = models.CharField(max_length=255, verbose_name=u'Nimi genetiivissä')

    description = models.TextField(blank=True, verbose_name=u'Kuvaus')
    homepage_url = models.CharField(blank=True, max_length=255, verbose_name=u'Kotisivu')
    muncipality = models.CharField(
        blank=True,
        max_length=127,
        verbose_name=u'Yhdistyksen kotipaikka',
        help_text=u'Kunta, johon yhdistys on rekisteröity.',
    )
    public = models.BooleanField(
        default=False,
        verbose_name=u'Julkinen',
        help_text=u'Julkisilla yhdistyksillä on yhdistyssivu ja ne näytetään etusivulla.',
    )

    logo_url = models.CharField(
        blank=True,
        max_length=255,
        default='',
        verbose_name=u'Organisaation logon URL',
        help_text=u'Voi olla paikallinen (alkaa /-merkillä) tai absoluuttinen (alkaa http/https)',
    )

    def save(self, *args, **kwargs):
        if self.name and not self.slug:
            self.slug = slugify(self.name)

        if self.name and not self.name_genitive:
            if self.name.endswith(u' ry'):
                self.name_genitive = self.name + u':n'
            else:
                self.name_genitive = self.name + u'n'

        return super(Organization, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

    @classmethod
    def get_or_create_dummy(cls):
        return cls.objects.get_or_create(
            slug='dummy-organization',
            defaults=dict(
                name='Dummy organization',
                homepage_url='http://example.com',
            )
        )

    @property
    def membership_organization_meta(self):
        if 'membership' not in settings.INSTALLED_APPS:
            return None

        from membership.models import MembershipOrganizationMeta

        try:
            return self.membershiporganizationmeta
        except MembershipOrganizationMeta.DoesNotExist:
            return None

    @property
    def access_organization_meta(self):
        if 'access' not in settings.INSTALLED_APPS:
            return None

        from access.models import AccessOrganizationMeta

        try:
            return self.accessorganizationmeta
        except AccessOrganizationMeta.DoesNotExist:
            return None

    def as_dict(self):
        return pick_attrs(self,
            'slug',
            'name',
            'homepage_url',
        )

    class Meta:
        verbose_name = u'Organisaatio'
        verbose_name_plural = u'Organisaatiot'
