from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save

from ..models import Entry


@receiver(pre_save, sender=Entry)
def before_entry_save(sender, instance, **kwargs):
    if instance.organization is None and instance.event is not None:
        instance.organization = instance.event.organization


@receiver(post_save, sender=Entry)
def on_entry_created(sender, instance, created, **kwargs):
    if not created:
        return

    instance.send_updates()
