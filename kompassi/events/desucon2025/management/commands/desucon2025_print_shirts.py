from django.core.management.base import BaseCommand

from kompassi.badges.emperkelators.desucon2025 import DesumPerkelator
from kompassi.core.models.event import Event


class Command(BaseCommand):
    help = "Print a list of shirt sizes for Desucon 2025"

    def handle(self, *args, **options):
        event_slug = "desucon2025"
        event = Event.objects.get(slug=event_slug)
        print("shirt_type,shirt_size,count")
        for shirt_type, shirt_size, count in DesumPerkelator.get_shirt_sizes(event):
            print(f"{shirt_type},{shirt_size},{count}")
