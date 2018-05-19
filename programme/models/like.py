from django.conf import settings
from django.db import models


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    programme = models.ForeignKey('programme.Programme')

    # denormalized
    event = models.ForeignKey('core.Event')

    class Meta:
        unique_together = [('user', 'event', 'programme')]
        index_together = [('event', 'programme')]
