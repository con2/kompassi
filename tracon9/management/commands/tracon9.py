# encoding: utf-8

from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType

from core.models import Event
from labour.models import EventMeta
from ...models import SignupExtra

class Command(BaseCommand):
    args = ''
    help = 'Setup tracon9 specific stuff'

    def handle(*args, **options):
    	content_type = ContentType.objects.get_for_model(SignupExtra)
    	event, unused = Event.objects.get_or_create(name="Tracon 9")
    	event_meta, unused = EventMeta.objects.get_or_create(event=event, signup_extra_content_type=content_type)