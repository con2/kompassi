# encoding: utf-8

from __future__ import unicode_literals, absolute_import

from django.dispatch import receiver
from django.db.models.signals import post_save

from ..models import Entry


@receiver(post_save, sender=Entry)
def on_entry_created(sender, instance, created, **kwargs):
    if not created:
        return

    instance.send_updates()
