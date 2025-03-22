from __future__ import annotations

from django.db import models


class ValueOrdering(models.TextChoices):
    MANUAL = "MANUAL", "Manual"
    SLUG = "SLUG", "Alphabetical (slug)"
    TITLE = "TITLE", "Alphabetical (localized title)"
