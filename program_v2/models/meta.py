from django.db import models
from core.models import EventMetaBase


class ProgramV2EventMeta(EventMetaBase):
    primary_dimension = models.ForeignKey(
        "program_v2.Dimension",
        on_delete=models.PROTECT,
        related_name="primary_dimension_for_event_meta",
        null=True,
        blank=True,
    )

    use_cbac = True
