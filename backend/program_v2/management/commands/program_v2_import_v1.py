import logging

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction

from core.models.event import Event
from dimensions.models.dimension import Dimension
from programme.models.category import Category
from programme.models.programme import Programme
from programme.models.room import Room
from programme.models.tag import Tag

from ...importers.default import DefaultImporter
from ...models.meta import ProgramV2EventMeta

logger = logging.getLogger("kompassi")


class NotReally(RuntimeError):
    pass


class Command(BaseCommand):
    args = "[event_slug...]"
    help = "Import program v1 data to v2"

    def add_arguments(self, parser):
        parser.add_argument(
            "event_slugs",
            nargs="*",
            metavar="EVENT_SLUG",
            default=[],  # mutable default, beware
        )

        parser.add_argument(
            "--all",
            action="store_true",
            default=False,
            help="Import all events that do not yet have Program V2 data.",
        )

        parser.add_argument(
            "--really",
            action="store_true",
            default=False,
        )

        parser.add_argument(
            "--dangerously-clear",
            action="store_true",
            default=False,
            help="Clear all existing program data before importing.",
        )

    def handle(*args, **opts):
        if opts["all"]:
            if opts["event_slugs"]:
                raise RuntimeError("Please specify either --all or event slugs, not both.")

            events = Event.objects.filter(programmeeventmeta__isnull=False, programv2eventmeta__isnull=True)
        else:
            events = Event.objects.filter(slug__in=opts["event_slugs"])

            if len(events) != len(opts["event_slugs"]):
                raise RuntimeError("Some events were not found.")

        for event in events:
            v1_meta = event.programme_event_meta
            v2_meta = event.program_v2_event_meta
            logger.info(
                "Starting programme import for %s with importer %s",
                event.slug,
                v2_meta.importer_name if v2_meta else "default",
            )
            queryset = Programme.objects.filter(category__event=event)

            try:
                with transaction.atomic():
                    if v2_meta is None:
                        importer = DefaultImporter(event)

                        # importing legacy event (may have duplicate slugs)
                        Programme.reslugify(queryset)

                        try:
                            room_dimension = Dimension.objects.get(universe=event.program_universe, slug="room")
                        except Dimension.DoesNotExist:
                            dimensions = importer.import_dimensions(
                                clear=opts["dangerously_clear"],
                                refresh_cached_dimensions=False,
                            )
                            room_dimension = next((d for d in dimensions if d.slug == "room"), None)

                        v2_meta, _ = ProgramV2EventMeta.objects.get_or_create(
                            event=event,
                            defaults=dict(
                                location_dimension=room_dimension,
                                importer_name="default",
                                admin_group=v1_meta.admin_group,
                                is_accepting_feedback=False,
                            ),
                        )

                        # default importer only sets tags based on v2_dimensions of the source
                        bulk_update_tags = []
                        for tag in Tag.objects.filter(event=event).select_for_update(of=("self",)):
                            if not tag.v2_dimensions:
                                tag.v2_dimensions = {"tag": [tag.slug]}
                                bulk_update_tags.append(tag)
                        Tag.objects.bulk_update(bulk_update_tags, ["v2_dimensions"])

                        bulk_update_categories = []
                        for category in Category.objects.filter(event=event).select_for_update(of=("self",)):
                            if not category.v2_dimensions:
                                category.v2_dimensions = {"category": [category.slug]}
                                bulk_update_categories.append(category)
                        Category.objects.bulk_update(bulk_update_categories, ["v2_dimensions"])

                        bulk_update_rooms = []
                        for room in Room.objects.filter(event=event).select_for_update(of=("self",)):
                            if not room.v2_dimensions:
                                room.v2_dimensions = {"room": [room.slug]}
                                bulk_update_rooms.append(room)
                        Room.objects.bulk_update(bulk_update_rooms, ["v2_dimensions"])

                        v1_meta.override_schedule_link = f"{settings.KOMPASSI_V2_BASE_URL}/{event.slug}/program"
                        v1_meta.save(update_fields=["override_schedule_link"])
                    else:
                        # this event may have paulig already in the database so respect the existing data
                        Importer = v2_meta.importer_class
                        if Importer is None:
                            raise TypeError(f"Importer class for {event.slug} is None.")
                        importer = Importer(event)

                        importer.import_dimensions(
                            clear=opts["dangerously_clear"],
                            refresh_cached_dimensions=False,
                        )

                    importer.import_program(
                        Programme.objects.filter(category__event=event),
                        clear=opts["dangerously_clear"],
                    )

                    if not opts["really"]:
                        raise NotReally("It was only a dream :')")
            except NotReally:
                logger.warning("DRY RUN: To actually save imported program, use --really.")
