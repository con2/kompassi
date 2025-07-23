from django.db.models.signals import pre_save
from django.dispatch import receiver

from kompassi.core.utils import slugify

from ..models import Role


@receiver(pre_save, sender=Role)
def role_pre_save(sender, instance, **kwargs):
    if instance.title and not instance.slug:
        instance.slug = slugify(instance.title)
