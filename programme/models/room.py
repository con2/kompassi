import logging
import os

from django.db import models
from django.db.models import Max
from django.db.transaction import atomic
from django.utils.translation import ugettext_lazy as _

from core.utils import NONUNIQUE_SLUG_FIELD_PARAMS


ROOM_NAME_MAX_LENGTH = 1023

logger = logging.getLogger('kompassi')


class Room(models.Model):
    event = models.ForeignKey('core.Event', on_delete=models.CASCADE, null=True, blank=True, related_name='rooms')
    name = models.CharField(max_length=ROOM_NAME_MAX_LENGTH)
    notes = models.TextField(blank=True)
    slug = models.CharField(**NONUNIQUE_SLUG_FIELD_PARAMS)

    paikkala_room = models.ForeignKey('paikkala.Room', on_delete=models.SET_NULL, null=True)

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
            name='Iso sali',
        )

    @property
    def can_delete(self):
        return not self.programmes.exists() and not self.view_rooms.exists()

    @property
    def has_paikkala_schema(self):
        return os.path.isfile(self.paikkala_schema_path)

    @property
    def paikkala_schema_path(self):
        from pkg_resources import resource_filename
        return resource_filename(__name__, f'paikkala_data/{self.event.venue.slug}/{self.slug}.csv')

    @atomic
    def paikkalize(self):
        from paikkala.models import Room as PaikkalaRoom
        from paikkala.utils.importer import read_csv, import_zones
        from uuid import uuid4

        if self.paikkala_room:
            logger.info('Room %s is alredy paikkalized, not re-paikkalizing', self)
            return self.paikkala_room

        # hack: dun wanna mess up with same-named rooms
        paikkala_room_name = str(uuid4())

        with open(self.paikkala_schema_path, 'r', encoding='UTF-8') as infp:
            import_zones(read_csv(infp), default_room_name=paikkala_room_name)

        self.paikkala_room = PaikkalaRoom.objects.get(name=paikkala_room_name)
        self.paikkala_room.name = self.name
        self.paikkala_room.save()
        self.save()

        return self.paikkala_room
