from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models


class FormResponse(models.Model):
    form = models.ForeignKey('forms.Form', on_delete=models.CASCADE)
    values = JSONField()

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
