import logging

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import HttpRequest
from django.shortcuts import get_object_or_404

from core.utils import get_ip

logger = logging.getLogger("kompassi")


def log_creations(model, **extra_kwargs_for_emit):
    """
    Sets up signal handlers so that whenever an instance of `model` is created, an Entry will be emitted.

    Extra keyword arguments will be passed to Entry. If the value of the keyword argument is a function,
    it will be called with the newly created instance to determine the value of the keyword argument to
    the Entry constructor.
    """
    # TODO Register the corresponding event type automatically. Now it needs to be registered by the caller.

    meta = model._meta
    entry_type_name = f"{meta.app_label}.{meta.model_name}.created"

    @receiver(post_save, sender=model, weak=False)
    def on_save_emit_event_log_entry(sender, instance, created, **kwargs):
        if not created:
            return

        kwargs_for_emit = dict()
        for key, value in extra_kwargs_for_emit.items():
            if callable(value):
                value = value(instance)

            kwargs_for_emit[key] = value

        emit(entry_type_name, **kwargs_for_emit)

    return on_save_emit_event_log_entry


def attrs_from_request(request: HttpRequest):
    from core.models import Event

    # from core.middleware
    event_slug: str | None = None
    organization_slug: str | None = None

    if resolver_match := request.resolver_match:
        if event_slug := resolver_match.kwargs.get("event_slug"):
            event = get_object_or_404(Event.objects.select_related("organization"), slug=event_slug)
            organization_slug = event.organization.slug
        else:
            organization_slug = resolver_match.kwargs.get("organization_slug")

    return dict(
        actor=request.user if request.user.is_authenticated else None,
        context=request.build_absolute_uri(request.get_full_path()),
        ip_address=get_ip(request),
        event=event_slug,
        organization=organization_slug,
    )


def emit(entry_type: str, **kwargs):
    """
    Records a log entry into the event log.

    `kwargs` are passed to the Entry constructor with the exception of the following special kwargs:

    * `request`: If present, sets fields that can be deduced from the request.
    """
    from ..models import Entry, Subscription

    if request := kwargs.pop("request", None):
        kwargs = dict(attrs_from_request(request), **kwargs)

    kwargs, other_fields = Entry.hoist(kwargs)
    logger.debug("event_log.utils.emit %s %s", entry_type, other_fields)

    entry = Entry(entry_type=entry_type, other_fields=other_fields, **kwargs)
    entry.save()

    for subscription in Subscription.objects.filter(entry_type=entry_type):
        subscription.send_update_for_entry(entry)
