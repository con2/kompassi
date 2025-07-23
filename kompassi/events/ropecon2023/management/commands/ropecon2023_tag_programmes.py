from django.core.management.base import BaseCommand

from kompassi.core.models import Event
from kompassi.zombies.programme.models import Programme, Tag

TAG_MAPPING = dict(
    is_english_ok="in-english",
    is_beginner_friendly="aloittelijaystavallinen",
    ropecon2022_aimed_at_children_under_10="suunnattu-alle-10-vuotiaille",
    ropecon2022_aimed_at_underage_participants="suunnattu-alaikaisille",
    ropecon2022_aimed_at_adult_participants="suunnattu-taysi-ikaisille",
    is_age_restricted="vain-taysi-ikaisille",
    ropecon_theme="teema-ystavyys",
)


class Command(BaseCommand):
    args = ""
    help = "Tag ropecon2023 programmes based on questions"

    def handle(self, *args, **opts):
        event = Event.objects.get(slug="ropecon2023")
        for field_name, tag_slug in TAG_MAPPING.items():
            tag = Tag.objects.get(event=event, slug=tag_slug)
            for programme in Programme.objects.filter(category__event=event, **{field_name: True}):
                programme.tags.add(tag)
                print(".", sep="", end="", flush=True)
        print()
