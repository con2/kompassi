from django.conf import settings
from django.contrib.postgres.fields import HStoreField
from django.db import models
from django.utils.timezone import now


class CBACEntry(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    valid_from = models.DateTimeField()
    valid_until = models.DateTimeField(null=True, blank=True)

    mode = models.CharField(
        max_length=1,
        choices=[('+', 'Allow'), ('-', 'Deny'), ('0', 'Inactive')],
        default='+',
    )

    claims = HStoreField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.valid_from:
            self.valid_from = now()

        return super().save(*args, **kwargs)
