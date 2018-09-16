# encoding: utf-8



import logging

from django.conf import settings

from core.utils import log_get_or_create
from programme.models import Category, Programme

from .models import Desuprogramme


logger = logging.getLogger('kompassi')


def import_programme(event, payload):
    if 'background_tasks' in settings.INSTALLED_APPS:
        from .tasks import import_programme as import_programme_task
        import_programme_task.delay(event.id, payload)
    else:
        _import_programme(event, payload)


def _import_programme(event, payload):
    assert event.programme_event_meta

    category, created = Category.objects.get_or_create(
        event=event,
        slug='desu',
        defaults=dict(
            title='Desusaitilta tuotu ohjelma',
            style='anime',
        )
    )

    desuprogrammes = [Desuprogramme.from_dict(programme_dict) for programme_dict in payload]

    # Make sure all listed programmes exist
    for programme_dict in payload:
        desuprogramme = Desuprogramme.from_dict(programme_dict)
        programme, created = desuprogramme.get_or_create(category=category)

        if not created:
            programme.state = 'accepted'
            programme.title = desuprogramme.title
            programme.description = desuprogramme.description
            programme.save()

        log_get_or_create(logger, programme, created)

    # Cancel removed programmes
    known_slugs = [desuprogramme.identifier for desuprogramme in desuprogrammes]
    for removed_programme in Programme.objects.filter(category=category).exclude(slug__in=known_slugs):
        logger.debug('Programme %s removed from Desusite, marking cancelled', removed_programme)
        removed_programme.state = 'cancelled'
        removed_programme.save()
        removed_programme.apply_state()

