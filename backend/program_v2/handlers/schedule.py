from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from ..models.schedule import ScheduleItem


@receiver(pre_save, sender=ScheduleItem)
def program_pre_save(sender, instance: ScheduleItem, **kwargs):
    if instance.start_time is not None and instance.length is not None:
        instance.cached_end_time = instance.start_time + instance.length


@receiver(post_save, sender=ScheduleItem)
def program_post_save(sender, instance: ScheduleItem, **kwargs):
    instance.program.refresh_cached_times()
