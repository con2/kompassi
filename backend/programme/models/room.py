from __future__ import annotations

import logging
from pathlib import Path
from typing import TYPE_CHECKING

from django.db import models
from django.db.transaction import atomic
from django.utils.translation import gettext_lazy as _

from core.models import Event
from core.utils import NONUNIQUE_SLUG_FIELD_PARAMS, slugify

if TYPE_CHECKING:
    from .programme import Programme
    from .schedule import ViewRoom

ROOM_NAME_MAX_LENGTH = 1023

logger = logging.getLogger("kompassi")


class Room(models.Model):
    id: int
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True, blank=True, related_name="rooms")
    name = models.CharField(max_length=ROOM_NAME_MAX_LENGTH)
    notes = models.TextField(blank=True)
    slug = models.CharField(**NONUNIQUE_SLUG_FIELD_PARAMS)  # type: ignore

    paikkala_room = models.ForeignKey(
        "paikkala.Room",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    v2_dimensions = models.JSONField(
        default=dict,
        blank=True,
        help_text=(
            "dimension slug -> list of dimension value slugs. "
            "When program is imported to v2, dimension values indicated here are added to programs of this category."
        ),
    )

    programmes: models.QuerySet[Programme]
    view_rooms: models.QuerySet[ViewRoom]

    def __str__(self):
        return self.name

    def programme_continues_at(self, the_time, **conditions):
        criteria = dict(start_time__lt=the_time, length__isnull=False, **conditions)

        latest_programme = self.programmes.filter(**criteria).order_by("-start_time")[:1]
        if latest_programme:
            return the_time < latest_programme[0].end_time
        else:
            return False

    class Meta:
        ordering = ["event", "name"]
        verbose_name = _("Room")
        verbose_name_plural = _("Rooms")
        unique_together = [
            ("event", "slug"),
        ]

    @classmethod
    def get_or_create_dummy(cls, event: Event | None = None):
        if event is None:
            event, unused = Event.get_or_create_dummy()

        return cls.objects.get_or_create(
            event=event,
            name="Iso sali",
        )

    @property
    def can_delete(self):
        return not self.programmes.exists() and not self.view_rooms.exists()

    @property
    def has_paikkala_schema(self):
        return self.paikkala_schema_path.exists()

    @property
    def paikkala_schema_path(self) -> Path:
        if not self.event:
            raise ValueError("Room %s has no event", self)

        return Path(__file__).parent / "paikkala_data" / self.event.venue.slug / f"{self.slug}.csv"

    @atomic
    def paikkalize(self):
        from uuid import uuid4

        from paikkala.models import Room as PaikkalaRoom
        from paikkala.utils.importer import import_zones, read_csv

        if self.paikkala_room:
            logger.info("Room %s is alredy paikkalized, not re-paikkalizing", self)
            return self.paikkala_room

        # hack: dun wanna mess up with same-named rooms
        paikkala_room_name = str(uuid4())

        with self.paikkala_schema_path.open(encoding="UTF-8") as infp:
            import_zones(row_csv_list=list(read_csv(infp)), default_room_name=paikkala_room_name)

        self.paikkala_room = PaikkalaRoom.objects.get(name=paikkala_room_name)
        self.paikkala_room.name = self.name
        self.paikkala_room.save()
        self.save()

        return self.paikkala_room

    def save(self, *args, **kwargs):
        if self.name and not self.slug:
            self.slug = slugify(self.name)

        if (
            self.slug
            and not self.v2_dimensions
            and self.event
            and (meta := self.event.program_v2_event_meta)
            and meta.importer_name == "default"
        ):
            self.v2_dimensions = {"room": [self.slug]}

        return super().save(*args, **kwargs)
