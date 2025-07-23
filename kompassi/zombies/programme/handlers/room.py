from django.db.models.signals import pre_save
from django.dispatch import receiver

from kompassi.core.utils import slugify

from ..models import Room


@receiver(pre_save, sender=Room)
def room_pre_save(sender, instance, **kwargs):
    if instance.name and not instance.slug:
        instance.slug = slugify(instance.name)
