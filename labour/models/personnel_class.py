# encoding: utf-8

from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.utils import NONUNIQUE_SLUG_FIELD_PARAMS, slugify


class PersonnelClass(models.Model):
    event = models.ForeignKey('core.Event')
    app_label = models.CharField(max_length=63, blank=True, default="")
    name = models.CharField(max_length=63)
    slug = models.CharField(**NONUNIQUE_SLUG_FIELD_PARAMS)
    perks = models.ManyToManyField('labour.Perk', blank=True)
    priority = models.IntegerField(default=0)

    class Meta:
        verbose_name = _(u'personnel class')
        verbose_name_plural = _(u'personnel classes')

        unique_together = [
            ('event', 'slug'),
        ]

        index_together = [
            ('event', 'app_label'),
        ]

        ordering = ('event', 'priority')

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.name and not self.slug:
            self.slug = slugify(self.name)

        return super(PersonnelClass, self).save(*args, **kwargs)