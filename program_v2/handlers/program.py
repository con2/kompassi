from django.dispatch import receiver
from django.db.models.signals import pre_save

from core.utils import slugify

from ..models import Program


@receiver(pre_save, sender=Program)
def program_pre_save(sender, instance, **kwargs):
    if instance.event is not None and instance.slug is None:
        instance.slug = slugify(instance.title)

    if instance.pk:
        instance.cached_dimensions = instance._dimensions
