from django.dispatch import receiver
from django.db.models.signals import pre_save

from ..models import Like


@receiver(pre_save, sender=Room)
def room_pre_save(sender, instance, **kwargs):
    instance.event = instance.programme.event if instance.programme else None
