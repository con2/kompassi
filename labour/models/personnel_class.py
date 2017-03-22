# encoding: utf-8



import logging

from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from core.utils import NONUNIQUE_SLUG_FIELD_PARAMS, slugify


logger = logging.getLogger('kompassi')


class PersonnelClass(models.Model):
    event = models.ForeignKey('core.Event')
    app_label = models.CharField(max_length=63, blank=True, default='labour')
    name = models.CharField(max_length=63)
    slug = models.CharField(**NONUNIQUE_SLUG_FIELD_PARAMS)
    perks = models.ManyToManyField('labour.Perk', blank=True)
    priority = models.IntegerField(default=0)

    class Meta:
        verbose_name = _('personnel class')
        verbose_name_plural = _('personnel classes')

        unique_together = [
            ('event', 'slug'),
        ]

        index_together = [
            ('event', 'app_label'),
        ]

        ordering = ('event', 'priority')

    @classmethod
    def get_or_create_dummy(cls, app_label='labour', name='Smallfolk', priority=0):
        from core.models import Event
        event, unused = Event.get_or_create_dummy()

        return PersonnelClass.objects.get_or_create(
            event=event,
            slug=slugify(name),
            app_label=app_label,
            defaults=dict(
                name=app_label,
                priority=priority,
            )
        )


    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.name and not self.slug:
            self.slug = slugify(self.name)

        return super(PersonnelClass, self).save(*args, **kwargs)
