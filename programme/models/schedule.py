# encoding: utf-8

from __future__ import unicode_literals

import logging
from datetime import timedelta

from django.contrib import messages
from django.db import models
from django.utils.translation import ugettext_lazy as _


logger = logging.getLogger('kompassi')

ONE_HOUR = timedelta(hours=1)


class ViewMethodsMixin(object):
    @property
    def programmes_by_start_time(self):
        return self.get_programmes_by_start_time()

    def get_programmes_by_start_time(self, include_unpublished=False, request=None):
        results = []
        prev_start_time = None
        cont_criteria = dict() if include_unpublished else dict(state='published')

        for start_time in self.start_times():
            cur_row = []
            criteria = dict(
                category__event=self.event,
                start_time=start_time,
                length__isnull=False,
            )

            if not include_unpublished:
                criteria.update(state='published')

            incontinuity = prev_start_time and (start_time - prev_start_time > ONE_HOUR)
            incontinuity = 'incontinuity' if incontinuity else ''
            prev_start_time = start_time

            results.append((start_time, incontinuity, cur_row))
            for room in self.rooms.all():
                programmes = room.programme_set.filter(**criteria)
                num_programmes = programmes.count()
                if num_programmes == 0:
                    if room.programme_continues_at(start_time, **cont_criteria):
                        # programme still continues, handled by rowspan
                        pass
                    else:
                        # there is no (visible) programme in the room at start_time, insert a blank
                        cur_row.append((None, None))
                else:
                    if programmes.count() > 1:
                        logger.warn('Room %s has multiple programs starting at %s', room, start_time)

                        if (
                            request is not None and
                            self.event.programme_event_meta.is_user_admin(request.user)
                        ):
                            messages.warning(request,
                                'Tilassa {room} on päällekkäisiä ohjelmanumeroita kello {start_time}'.format(
                                    room=room,
                                    start_time=format_datetime(start_time.astimezone(tzlocal())),
                                )
                            )

                    programme = programmes.first()

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
            result = [
                i for i in result if
                    programme.start_time <= i < programme.end_time
            ]

        return sorted(set(result))

    def rowspan(self, programme):
        return len(self.start_times(programme=programme))


class View(models.Model, ViewMethodsMixin):
    event = models.ForeignKey('core.Event')
    name = models.CharField(max_length=32)
    public = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    rooms = models.ManyToManyField('programme.Room')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('schedule view')
        verbose_name_plural = _('schedule views')
        ordering = ['event', 'order']


class AllRoomsPseudoView(ViewMethodsMixin):
    def __init__(self, event):
        from .room import Room

        self.name = _('All rooms')
        self.public = True
        self.order = 0
        self.rooms = Room.objects.filter(venue=event.venue, view__event=event)
        self.event = event


class TimeBlock(models.Model):
    event = models.ForeignKey('core.event')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()


class SpecialStartTime(models.Model):
    event = models.ForeignKey('core.event', verbose_name=_('event'))
    start_time = models.DateTimeField(verbose_name=_('starting time'))

    def __unicode__(self):
        from core.utils import format_datetime
        return format_datetime(self.start_time) if self.start_time else 'None'

    class Meta:
        verbose_name = _('special start time')
        verbose_name_plural = _('special start times')
        ordering = ['event', 'start_time']
        unique_together = [
            ('event', 'start_time'),
        ]
