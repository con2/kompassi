from django.db.models.signals import pre_save
from django.dispatch import receiver

from ..models import View


@receiver(pre_save, sender=View)
def view_pre_save(sender, instance, **kwargs):
    if instance.event is not None and instance.order is None:
        instance.order = instance.get_next_order(event=instance.event)
