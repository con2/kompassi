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

        content_type = ContentType.objects.get_for_model(JVKortti)
        Qualification.objects.get_or_create(
            slug='jv-kortti',
            defaults=dict(
                name=u"JV-kortti",
                qualification_extra_content_type=content_type
            )
        )

        for slug, name in [
            ('b-ajokortti', u"Henkilöauton ajokortti (B)"),
            ('c-ajokortti', u"Kuorma-auton ajokortti (C)"),
            ('ea1', u"Ensiapukoulutus EA1"),
            ('ea2', u"Ensiapukoulutus EA2"),
            ('hygieniapassi', u"Hygieniapassi"),
        ]:
            Qualification.objects.get_or_create(slug=slug, defaults=dict(name=name))