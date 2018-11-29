# encoding: utf-8

from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.utils import NONUNIQUE_SLUG_FIELD_PARAMS, slugify


class Perk(models.Model):
    event = models.ForeignKey('core.Event', on_delete=models.CASCADE)
    slug = models.CharField(**NONUNIQUE_SLUG_FIELD_PARAMS)
    name = models.CharField(max_length=63)

    class Meta:
        verbose_name = _('perk')
        verbose_name_plural = _('perks')

        unique_together = [
            ('event', 'slug'),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.name and not self.slug:
            self.slug = slugify(self.name)

        return super(Perk, self).save(*args, **kwargs)
