from django.core.management.base import BaseCommand
from django.db import transaction

from programme.models import Programme
from paikkala.models import Program as PaikkalaProgram, Room as PaikkalaRoom, Zone as PaikkalaZone
from core.models import Event
from programme.models.room import Room


class NotReally(RuntimeError):
    pass


class Command(BaseCommand):
    args = "[event_slug...]"
    help = "Create missing badges for programme"

    def add_arguments(self, parser):
        parser.add_argument(
            "event_slugs",
            nargs="+",
            metavar="EVENT_SLUG",
        )

        parser.add_argument(
            "--really",
            default=False,
            action="store_true",
        )

    def handle(*args, **opts):
        for event_slug in opts["event_slugs"]:
            try:
                with transaction.atomic():
                    event = Event.objects.get(slug=event_slug)

                    ps = Programme.objects.filter(category__event=event, is_using_paikkala=True)
                    num_ps = ps.distinct().count()
                    p_ids = list(ps.distinct().values_list("id", flat=True))

                    rooms = Room.objects.filter(programmes__in=ps).distinct()
                    num_rooms = rooms.distinct().count()

                    pps = PaikkalaProgram.objects.filter(kompassi_programme__in=ps)
                    prooms = PaikkalaRoom.objects.filter(program__in=pps)
                    pzones = PaikkalaZone.objects.filter(room__in=prooms)

                    print(rooms.distinct())
                    print(pps.distinct())
                    print(prooms.distinct())
                    print(pzones.distinct())

                    ps.update(paikkala_program=None)
                    rooms.update(paikkala_room=None)

                    pps.delete()
                    pzones.delete()
                    prooms.delete()

                    ps = Programme.objects.filter(id__in=p_ids)
                    ps.update(is_using_paikkala=True)
                    for programme in ps.all():
                        programme.paikkalize()

                    pps = PaikkalaProgram.objects.filter(kompassi_programme__in=ps.all())
                    prooms = PaikkalaRoom.objects.filter(program__in=pps).distinct()
                    pzones = PaikkalaZone.objects.filter(room__in=prooms).distinct()

                    print(pps)
                    print(prooms)
                    print(pzones)

                    # I am paranoid about runaway cascades
                    assert ps.distinct().count() == num_ps
                    assert rooms.distinct().count() == num_rooms

                    if not opts["really"]:
                        raise NotReally()
            except NotReally:
                pass
