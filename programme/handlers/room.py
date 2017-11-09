from django.dispatch import receiver
from django.db.models.signals import pre_save

from core.utils import slugify

from ..models import Room


@receiver(pre_save, sender=Room)
def room_pre_save(sender, instance, **kwargs):
    if instance.order is None and instance.event is not None:
        instance.order = Room.get_next_order(instance.event)

    if instance.name and not instance.slug:
        instance.slug = slugify(instance.name)
