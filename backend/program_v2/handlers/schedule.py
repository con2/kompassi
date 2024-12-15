from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from ..models.schedule import ScheduleItem


@receiver(pre_save, sender=ScheduleItem)
def program_pre_save(sender, instance: ScheduleItem, **kwargs):
    instance.with_generated_fields()


@receiver(post_save, sender=ScheduleItem)
def program_post_save(sender, instance: ScheduleItem, **kwargs):
    if kwargs.get("update_fields", {}):
        return

    instance.program.refresh_cached_fields_from_schedule_items()
