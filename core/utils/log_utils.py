# encoding: utf-8


def log_get_or_create(logger, obj, created):
    logger.info(u'{kind} {name} {what_done}'.format(
        kind=obj.__class__.__name__,
        name=unicode(obj),
        what_done=u'created' if created else u'already exists',
    ))