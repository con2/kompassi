# encoding: utf-8

from __future__ import unicode_literals

import logging

from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import Entry


logger = logging.getLogger('kompassi')
INSTANCE = object()


def log_creations(model, **extra_kwargs_for_emit):
    meta = model._meta
    entry_type_name = '{app_label}.{model_name}.created'.format(
        app_label=meta.app_label,
        model_name=meta.model_name,
    )

    @receiver(post_save, sender=model, weak=False)
    def on_save_emit_event_log_entry(sender, instance, created, **kwargs):
        if not created:
            return

        kwargs_for_emit = dict()
        for key, value in extra_kwargs_for_emit.iteritems():
            if value is INSTANCE:
                value = instance
            elif callable(value):
                value = value(instance)

            kwargs_for_emit[key] = value

        emit(entry_type_name, **kwargs_for_emit)

    return on_save_emit_event_log_entry


def emit(entry_type_name, **kwargs):
    entry = Entry(entry_type=entry_type_name, **kwargs)
    entry.save()
