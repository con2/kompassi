import sys

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    args = ""
    help = "Make sure all users belong to their respective labour groups"

    def handle(*args, **options):
        from kompassi.labour.models import Signup

        for signup in Signup.objects.all():
            signup.apply_state()
            sys.stdout.write(".")
            sys.stdout.flush()

        print()
