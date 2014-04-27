# encoding: utf-8

# Enable johnny-cache for workers etc.
from johnny.cache import enable as enable_johnny_cache
enable_johnny_cache()

from django.core.management.base import BaseCommand

from programme.models import Programme

class Command(BaseCommand):
    args = ''
    help = 'Fix dashes in programme descriptions'

    def handle(*args, **options):
      for programme in Programme.objects.all():
        if u' - ' in programme.title or u' - ' in programme.description:
          programme.title = programme.title.replace(u' - ', u' – ')
          programme.description = programme.description.replace(u' - ', u' – ')
          programme.save()