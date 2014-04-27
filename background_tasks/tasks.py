from __future__ import absolute_import

# Enable johnny-cache for workers etc.
from johnny.cache import enable as enable_johnny_cache
enable_johnny_cache()

from celery import shared_task


@shared_task
def ping():
    return "pong"
