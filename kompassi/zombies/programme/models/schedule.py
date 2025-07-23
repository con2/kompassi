import logging
from collections import defaultdict
from datetime import timedelta
from typing import Any

from dateutil.tz import tzlocal
from django.contrib import messages
from django.db import models
from django.db.models import Max, QuerySet
from django.utils.translation import gettext_lazy as _

from kompassi.core.utils import format_datetime, get_previous_and_next

from .programme import Programme
from .room import Room

logger = logging.getLogger(__name__)

ONE_HOUR = timedelta(hours=1)


class OrderingMixin:
    objects: Any

    @classmethod
    def get_next_order(cls, **kwargs):
        cur_max_value = cls.objects.filter(**kwargs).aggregate(Max("order"))["order__max"] or 0
        return cur_max_value + 10

    def move(self, queryset, direction):
        try:
            if direction in ["left", "up", "previous", "back"]:
                swappee, unused = get_previous_and_next(queryset, self)
            elif direction in ["right", "down", "next", "forward"]:
                unused, swappee = get_previous_and_next(queryset, self)
            else:
                raise AssertionError(f"Invalid direction: {direction}")
        except self.__class__.DoesNotExist as dne:
            raise IndexError(f"Cannot go {direction} from here") from dne

        if self.order == swappee.order:
            raise ValueError(f"Unable to swap because {self} and {swappee} have same order: {self.order}")

        self.order, swappee.order = swappee.order, self.order
        self.save()
        swappee.save()


class ViewMethodsMixin:
    @property
    def programmes_by_start_time(self):
        return self.get_programmes_by_start_time()

    def get_programmes_by_start_time(self, include_unpublished=False, request=None):
        results = []
        prev_start_time = None
        cont_criteria = dict() if include_unpublished else dict(state="published")
        rooms = self.rooms.all()

        criteria = dict(
            category__event=self.event,
            length__isnull=False,
            start_time__isnull=False,
            room__in=rooms,
        )
        if not include_unpublished:
            criteria.update(state="published")

        # programme_index[start_time][room] = list of programmes
        # TODO select_related
        programme_index = defaultdict(lambda: defaultdict(list))
        programmes = (
            Programme.objects.filter(**criteria)
            .select_related("category__event")
            .select_related("room")
            .prefetch_related("tags")
        )
        for programme in programmes:
            programme_index[programme.start_time][programme.room_id].append(programme)

        for start_time in self.start_times():
            cur_row = []

            incontinuity = prev_start_time and (start_time - prev_start_time > ONE_HOUR)
            incontinuity = "incontinuity" if incontinuity else ""
            prev_start_time = start_time

            results.append((start_time, incontinuity, cur_row))
            for room in rooms:
                programmes = programme_index[start_time][room.id]
                num_programmes = len(programmes)
                if num_programmes == 0:
                    if room.programme_continues_at(start_time, **cont_criteria):
                        # programme still continues, handled by rowspan
                        pass
                    else:
                        # there is no (visible) programme in the room at start_time, insert a blank
                        cur_row.append((None, None))
                else:
                    if num_programmes > 1:
                        logger.warning("Room %s has multiple programs starting at %s", room, start_time)

                        if request is not None and self.event.programme_event_meta.is_user_admin(request.user):
                            messages.warning(
                                request,
                                f"Tilassa {room} on päällekkäisiä ohjelmanumeroita kello {format_datetime(start_time.astimezone(tzlocal()))}",
                            )

                    programme = programmes[0]

                    rowspan = self.rowspan(programme)
                    cur_row.append((programme, rowspan))

        return results

    def start_times(self, programme=None):
        result = [t.start_time for t in SpecialStartTime.objects.filter(event=self.event)]

        for time_block in TimeBlock.objects.filter(event=self.event):
            cur = time_block.start_time
            while cur <= time_block.end_time:
                result.append(cur)
                cur += ONE_HOUR

        if programme:
            result = [i for i in result if programme.start_time <= i < programme.end_time]

        if self.start_time:
            result = [i for i in result if i >= self.start_time]

        if self.end_time:
            result = [i for i in result if i < self.end_time]

        return sorted(set(result))

    def rowspan(self, programme):
        return len(self.start_times(programme=programme))


class View(models.Model, ViewMethodsMixin, OrderingMixin):
    event = models.ForeignKey("core.Event", on_delete=models.CASCADE, related_name="views")
    name = models.CharField(max_length=32, verbose_name=_("Title"))
    public = models.BooleanField(
        default=True,
        verbose_name=_("Visible"),
        help_text=_("Even if the schedule is already published, you can hide this view by unchecking this box."),
    )
    order = models.IntegerField(help_text=_("This will be automatically filled in if not provided."))
    start_time = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Start time"),
    )
    end_time = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("End time"),
        help_text=_(
            "If the start and end times are set, this view will be constrained to those times. "
            "Use this for eg. day-specific views. If these are not set, the whole event will be "
            "displayed in a single view."
        ),
    )

    @property
    def rooms(self):
        from .room import Room

        return Room.objects.filter(view_rooms__view=self).order_by("view_rooms__order")

    @rooms.setter
    def rooms(self, rooms):
        self.view_rooms.all().delete()
        for order, room in enumerate(rooms, 1):
            ViewRoom.objects.create(
                view=self,
                room=room,
                order=order * 10,
            )

    def __str__(self):
        return self.name

    def get_form(self, *args, **kwargs):
        from ..forms import ViewForm

        return ViewForm(*args, **kwargs, instance=self)

    def get_add_room_form(self, *args, **kwargs):
        from ..forms import AddRoomForm

        return AddRoomForm(*args, **kwargs, instance=self)

    class Meta:
        verbose_name = _("schedule view")
        verbose_name_plural = _("schedule views")
        ordering = ["event", "order"]


class ViewRoom(models.Model, OrderingMixin):
    view = models.ForeignKey("programme.View", on_delete=models.CASCADE, related_name="view_rooms")
    room = models.ForeignKey("programme.Room", on_delete=models.CASCADE, related_name="view_rooms")
    order = models.IntegerField(help_text=_("This will be automatically filled in if not provided."))

    @property
    def event(self):
        return self.view.event if self.view is not None else None

    def admin_get_event(self):
        return self.event

    admin_get_event.short_description = _("Event")
    admin_get_event.admin_order_field = "view__event"

    def __str__(self):
        return f"{self.view} / {self.room}"

    class Meta:
        ordering = ["view", "order"]


class AllRoomsPseudoView(ViewMethodsMixin):
    def __init__(self, event, rooms: QuerySet[Room] | None = None):
        if rooms is None:
            rooms = Room.objects.filter(event=event)

        self.name = _("All rooms")
        self.public = True
        self.order = 0
        self.rooms = rooms
        self.event = event
        self.start_time = None
        self.end_time = None


class TimeBlock(models.Model):
    event = models.ForeignKey("core.event", on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()


class SpecialStartTime(models.Model):
    event = models.ForeignKey("core.event", on_delete=models.CASCADE, verbose_name=_("event"))
    start_time = models.DateTimeField(verbose_name=_("starting time"))

    def __str__(self):
        from kompassi.core.utils import format_datetime

        return format_datetime(self.start_time) if self.start_time else "None"

    class Meta:
        verbose_name = _("special start time")
        verbose_name_plural = _("special start times")
        ordering = ["event", "start_time"]
        unique_together = [
            ("event", "start_time"),
        ]
