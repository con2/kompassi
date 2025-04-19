from dataclasses import dataclass
from functools import cached_property

from django.conf import settings
from django.db import models

from core.models.event_meta_base import EventMetaBase
from core.models.person import Person
from dimensions.models.dimension import Dimension
from dimensions.models.universe import Universe
from forms.models.response import Response

IMPORTER_CHOICES = [
    ("default", "Default"),
    ("solmukohta2024", "Solmukohta 2024"),
]


class ProgramV2EventMeta(EventMetaBase):
    location_dimension = models.ForeignKey(
        Dimension,
        on_delete=models.PROTECT,
        related_name="location_dimension_for_event_meta",
        null=True,
        blank=True,
        help_text=(
            "If set, this dimension will be used as the location dimension for the event. "
            "This is used at least by the calendar export for the iCalendar location field."
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

    is_accepting_feedback = models.BooleanField(
        default=True,
        verbose_name="Is accepting feedback",
        help_text="If checked, feedback can be left for programs.",
    )

    use_cbac = True

    def __str__(self):
        return str(self.event)

    @property
    def importer_class(self):
        from ..importers.default import DefaultImporter
        from ..importers.hitpoint2024 import HitpointImporter
        from ..importers.noop import NoopImporter
        from ..importers.ropecon2024 import RopeconImporter
        from ..importers.tracon2024 import TraconImporter

        match self.importer_name:
            case "":
                return None
            case "default":
                return DefaultImporter
            case "noop":
                return NoopImporter
            case "ropecon2024":
                return RopeconImporter
            case "tracon2024":
                return TraconImporter
            case "hitpoint2024":
                return HitpointImporter
            case unimplemented_importer_name:
                raise NotImplementedError(unimplemented_importer_name)

    @property
    def is_auto_importing_from_v1(self):
        return self.importer_name != ""

    @cached_property
    def universe(self) -> Universe:
        from program_v2.workflow import ProgramOfferWorkflow

        return ProgramOfferWorkflow.get_program_universe(self.event)

    @property
    def program_offers(self):
        return Response.objects.filter(
            form__event=self.event,
            form__survey__app="program_v2",
        )

    @property
    def schedule_url(self):
        return f"{settings.KOMPASSI_V2_BASE_URL}/{self.event.slug}/program"


@dataclass
class ProgramV2ProfileMeta:
    """
    No need for an actual model for now. This serves as a stand-in for GraphQL.
    """

    person: Person
