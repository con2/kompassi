# encoding: utf-8

from django.db import models
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

from core.utils import NONUNIQUE_SLUG_FIELD_PARAMS, slugify, url
from core.models import OneTimeCode, OneTimeCodeLite


class Role(models.Model):
    title = models.CharField(max_length=1023)
    require_contact_info = models.BooleanField(default=True)
    is_default = models.BooleanField(default=False)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _(u'role')
        verbose_name_plural = _(u'roles')
        ordering = ['title']

    @classmethod
    def get_or_create_dummy(cls):
        return cls.objects.get_or_create(
            title=u'Overbaron',
            require_contact_info=False
        )





