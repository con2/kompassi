from django.db import models

from backend.models import Programme, Room


class ViewMethodsMixin(object):
    @property
    def programmes_by_start_time(self):
        results = []
        for start_time in self.start_times(public=True, room__public=True):
            cur_row = []
            results.append((start_time, cur_row))
            for room in self.rooms.filter(public=True):
                try:
                    programme = room.programme_set.get(
                        start_time=start_time,
                        public=True,
                        room__public=True
                    )
                    rowspan = self.rowspan(programme)
                    cur_row.append((programme, rowspan))
                except Programme.DoesNotExist:
                    if room.programme_continues_at(start_time):
                        # programme still continues, handled by rowspan
                        pass
                    else:
                        # there is no (visible) programme in the room at start_time, insert a blank
                        cur_row.append((None, None))
                except Programme.MultipleObjectsReturned:
                    raise ValueError('Room {room} has multiple programs starting at {start_time}'.format(**locals()))

        return results

    def start_times(self, **conditions):
        return sorted(list(set(p.start_time for p in Programme.objects.filter(room__in=self.public_rooms, **conditions))))

    @property
    def public_rooms(self):
        return self.rooms.filter(public=True)

    def rowspan(self, programme):
        return len(self.start_times(
            start_time__gte=programme.start_time,
            start_time__lt=programme.end_time,
            public=True
        ))


class View(models.Model, ViewMethodsMixin):
    name = models.CharField(max_length=32)
    public = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    rooms = models.ManyToManyField(Room)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['order']


class AllRoomsPseudoView(ViewMethodsMixin):
    def __init__(self):
        self.name = 'All rooms'
        self.public = True
        self.order = 0
        self.rooms = Room.objects.all()