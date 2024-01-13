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

    skip_offer_form_selection = models.BooleanField(
        default=False,
        verbose_name="Skip offer form selection",
        help_text=(
            "If checked, the user will not be able to choose an offer form. "
            "Instead they will be redirected to the default offer form."
        ),
    )

    use_cbac = True
