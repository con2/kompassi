# encoding: utf-8



from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.utils import NONUNIQUE_SLUG_FIELD_PARAMS, slugify


class Tag(models.Model):
    event = models.ForeignKey('core.Event', on_delete=models.CASCADE)
    slug = models.CharField(**NONUNIQUE_SLUG_FIELD_PARAMS)

    title = models.CharField(max_length=63)
    order = models.IntegerField(default=0)
    style = models.CharField(max_length=15, default='label-default')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.title and not self.slug:
            self.slug = slugify(self.title)

        return super(Tag, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _('tag')
        verbose_name_plural = _('tags')
        ordering = ['order']
        unique_together = [
            ('event', 'slug'),
        ]
