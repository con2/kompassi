from django.db import models
from django.db.models import Max
from django.utils.translation import ugettext_lazy as _

from core.utils import NONUNIQUE_SLUG_FIELD_PARAMS


ROOM_NAME_MAX_LENGTH = 1023


class Room(models.Model):
    event = models.ForeignKey('core.Event', on_delete=models.CASCADE, null=True, blank=True, related_name='rooms')
    name = models.CharField(max_length=ROOM_NAME_MAX_LENGTH)
    notes = models.TextField(blank=True)
    slug = models.CharField(**NONUNIQUE_SLUG_FIELD_PARAMS)

    def __str__(self):
        return self.name

    def programme_continues_at(self, the_time, **conditions):
        criteria = dict(
            start_time__lt=the_time,
            length__isnull=False,
            **conditions
        )

        latest_programme = self.programmes.filter(**criteria).order_by('-start_time')[:1]
        if latest_programme:
            return the_time < latest_programme[0].end_time
        else:
            return False

    class Meta:
        ordering = ['event', 'name']
        verbose_name = _('Room')
        verbose_name_plural = _('Rooms')
        unique_together = [
            ('event', 'slug'),
        ]

    @classmethod
    def get_or_create_dummy(cls):
        from core.models import Event
        event, unused = Event.get_or_create_dummy()
        return cls.objects.get_or_create(
            event=event,
            name='Dummy room',
        )

    @property
    def can_delete(self):
        return not self.programmes.exists() and not self.view_rooms.exists()
