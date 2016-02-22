# encoding: utf-8

from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from core.utils import NONUNIQUE_SLUG_FIELD_PARAMS, slugify


class Room(models.Model):
    venue = models.ForeignKey('core.Venue')
    name = models.CharField(max_length=1023)
    order = models.IntegerField()
    notes = models.TextField(blank=True)
    slug = models.CharField(**NONUNIQUE_SLUG_FIELD_PARAMS)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name

    def programme_continues_at(self, the_time, **conditions):
        criteria = dict(
            start_time__lt=the_time,
            length__isnull=False,
            **conditions
        )

        latest_programme = self.programme_set.filter(**criteria).order_by('-start_time')[:1]
        if latest_programme:
            return the_time < latest_programme[0].end_time
        else:
            return False

    class Meta:
        ordering = ['venue', 'order']
        verbose_name = u'tila'
        verbose_name_plural = u'tilat'
        unique_together = [
            ('venue', 'order'),
            ('venue', 'slug'),
        ]

    @classmethod
    def get_or_create_dummy(cls):
        from core.models import Venue
        venue, unused = Venue.get_or_create_dummy()
        return cls.objects.get_or_create(
            venue=venue,
            name=u'Dummy room',
            defaults=dict(
                order=0,
            )
        )


@receiver(pre_save, sender=Room)
def populate_room_slug(sender, instance, **kwargs):
    if instance.name and not instance.slug:
        instance.slug = slugify(instance.name)
