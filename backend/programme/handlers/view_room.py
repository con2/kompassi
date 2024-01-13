from django.db.models.signals import pre_save
from django.dispatch import receiver

from ..models import ViewRoom


@receiver(pre_save, sender=ViewRoom)
def view_room_pre_save(sender, instance, **kwargs):
    if instance.view is not None and instance.order is None:
        instance.order = instance.get_next_order(view=instance.view)
