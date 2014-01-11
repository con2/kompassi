# encoding: utf-8

from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType

from labour.models import Qualification
from ...models import JVKortti

class Command(BaseCommand):
    args = ''
    help = 'Setup common labour qualifications'

    def handle(*args, **options):
        if options['test']:
            print 'Setting up labour_common_qualifications in test mode'
        else:
            print 'Setting up labour_common_qualifications in production mode'

        for model in [JVKortti]:
            content_type = ContentType.objects.get_for_model(model)
            Qualification.objects.get_or_create(
                slug='jvkortti',
                defaults=dict(
                    name=u"JV-kortti",
                    qualification_extra_content_type=content_type
                )
            )