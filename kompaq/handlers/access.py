# encoding: utf-8

from __future__ import unicode_literals, absolute_import

from django.dispatch import receiver
from django.db.models.signals import post_save

from access.models import SMTPPassword

from ..utils import send_update


@receiver(post_save, sender=SMTPPassword)
def on_smtppassword_created(sender, instance, created, **kwargs):
    if not created:
        return

    send_update(instance, 'created')
