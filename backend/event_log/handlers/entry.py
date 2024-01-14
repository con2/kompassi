from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from core.models import Event, Organization, Person

from ..models import Entry


@receiver(pre_save, sender=Entry)
def before_entry_save(sender, instance, **kwargs):
    if claims := instance.other_fields.get("claims", {}):
        if instance.event is None:  # noqa: SIM102
            if event_slug := claims.get("event"):
                instance.event = Event.objects.filter(slug=event_slug).first()
        if instance.organization is None:  # noqa: SIM102
            if organization_slug := claims.get("organization"):
                instance.organization = Organization.objects.filter(slug=organization_slug).first()

    if instance.organization is None and instance.event is not None:
        instance.organization = instance.event.organization

    if instance.person is None:  # noqa: SIM102
        if username := instance.other_fields.get("user"):  # noqa: SIM102
            if user := get_user_model().objects.filter(username=username).first():
                try:
                    instance.person = user.person
                except Person.DoesNotExist:
                    pass


@receiver(post_save, sender=Entry)
def on_entry_created(sender, instance, created, **kwargs):
    if not created:
        return

    instance.send_updates()
