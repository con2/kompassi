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
    is_public = models.BooleanField(
        default=True,
        verbose_name=_(u'Public'),
        help_text=_(u'Only hosts who are assigned public roles will be shown publicly in the programme schedule.'),
    )

    priority = models.IntegerField(
        default=0,
        verbose_name=_(u'Priority'),
        help_text=_(u'If a host is involved in multiple Programmes in a single event, to determine their entitlement to a badge and other perks, lowest priority number wins.')
    )
    personnel_class = models.ForeignKey('labour.PersonnelClass',
        null=True,
        blank=True,
        verbose_name=_(u'Personnel class'),
        help_text=_(u'If the members of this programme role should have a badge, please point this field to their personnel class.'),
    )

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _(u'role')
        verbose_name_plural = _(u'roles')
        ordering = ('priority', 'title')

    @classmethod
    def get_or_create_dummy(cls):
        return cls.objects.get_or_create(
            title=u'Overbaron',
            require_contact_info=False
        )





