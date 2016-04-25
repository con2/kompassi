# encoding: utf-8

from django.db import models
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from core.utils import NONUNIQUE_SLUG_FIELD_PARAMS, slugify


class Tag(models.Model):
    event = models.ForeignKey('core.Event')
    title = models.CharField(max_length=63)
    order = models.IntegerField(default=0)
    style = models.CharField(max_length=15, default='label-default')

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _(u'tag')
        verbose_name_plural = _(u'tags')
        ordering = ['order']
