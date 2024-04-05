from django.db import models

from core.models import EventMetaBase

IMPORTER_CHOICES = [
    ("default", "Default"),
    ("solmukohta2024", "Solmukohta 2024"),
]


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

    importer_name = models.CharField(
        default="",
        blank=True,
        max_length=max(len(key) for key, _ in IMPORTER_CHOICES),
        choices=IMPORTER_CHOICES,
        verbose_name="V1 program importer",
        help_text=(
            "Select the importer to use when importing program data from v1. "
            "WARNING: If set, destructive changes will be made to the v2 program data. "
            "Do not set for events that are using Program v2 natively."
        ),
    )

    use_cbac = True

    @property
    def importer(self):
        from ..importers.default import import_default
        from ..importers.solmukohta2024 import import_solmukohta2024

        match self.importer_name:
            case "solmukohta2024":
                return import_solmukohta2024
            case _:
                return import_default

    @property
    def is_auto_importing_from_v1(self):
        return self.importer_name != ""
