# encoding: utf-8

from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from core.utils import NONUNIQUE_SLUG_FIELD_PARAMS, slugify


class Category(models.Model):
    event = models.ForeignKey('core.Event', on_delete=models.CASCADE)
    title = models.CharField(max_length=1023)
    slug = models.CharField(**NONUNIQUE_SLUG_FIELD_PARAMS)
    style = models.CharField(max_length=15)
    notes = models.TextField(blank=True)
    public = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']
        unique_together = [('event', 'slug')]
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    @classmethod
    def get_or_create_dummy(cls):
        from .programme_event_meta import ProgrammeEventMeta

        meta, unused = ProgrammeEventMeta.get_or_create_dummy()

        return cls.objects.get_or_create(
            event=meta.event,
            title='Dummy category',
            defaults=dict(
                style='dummy',
            )
        )


@receiver(pre_save, sender=Category)
def populate_category_slug(sender, instance, **kwargs):
    if instance.title and not instance.slug:
        instance.slug = slugify(instance.title)
