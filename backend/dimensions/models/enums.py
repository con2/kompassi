from __future__ import annotations

from enum import Enum

from django.db import models


class ValueOrdering(models.TextChoices):
    MANUAL = "MANUAL", "Manual"
    SLUG = "SLUG", "Alphabetical (slug)"
    TITLE = "TITLE", "Alphabetical (localized title)"


class DimensionApp(Enum):
    FORMS = "forms"
    PROGRAM_V2 = "program_v2"
    INVOLVEMENT = "involvement"
