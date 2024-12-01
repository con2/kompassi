from __future__ import annotations

from django.db import models


class ValueOrdering(models.TextChoices):
    MANUAL = "manual", "Manual"
    SLUG = "slug", "Alphabetical (slug)"
    TITLE = "title", "Alphabetical (localized title)"
