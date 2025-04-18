import logging
from collections.abc import Sequence

from core.models.event import Event
from dimensions.models.dimension import Dimension
from dimensions.models.dimension_dto import DimensionDTO, DimensionValueDTO, ValueOrdering
from dimensions.models.universe import Universe
from forms.models.response import Response
from forms.models.survey import Survey
from forms.models.workflow import Workflow

from .models.program import Program

logger = logging.getLogger("kompassi")


class ProgramOfferWorkflow(Workflow, arbitrary_types_allowed=True):
    """
    Workflow for program offers. This workflow is used to set the state of the program offer
    and possibly other automated actions in the future.
    """

    slug: str = "program_offer"
    survey: Survey

    @classmethod
    def get_program_universe(cls, event: Event) -> Universe:
        """
        Returns the universe for the program offer workflow.
        """
        universe, created = Universe.objects.get_or_create(
            scope=event.scope,
            slug="program",
            app="program_v2",
        )

        if created:
            cls._setup_default_dimensions(universe)

        return universe

    @classmethod
    def backfill_default_dimensions(cls, event: Event) -> None:
        """
        Backfills the default dimensions for the program offer workflow.
        Use this method to migrate events that had Program V2 initialized
        before April 2025.
        """
        logger.info("Backfilling default dimensions for event %s", event.slug)

        universe = cls.get_program_universe(event)
        cls._setup_default_dimensions(universe)

        for program_offer in Response.objects.filter(
            form__event=event,
            form__survey__app="program_v2",
        ):
            values = ["accepted"] if program_offer.programs.exists() else ["new"]
            program_offer.set_dimension_values({"state": values})

        for program in Program.objects.filter(event=event):
            program.set_dimension_values({"state": ["accepted"]})

        Program.refresh_cached_dimensions_qs(Program.objects.filter(event=event))

    @classmethod
    def _setup_default_dimensions(cls, universe: Universe) -> Sequence[Dimension]:
        return DimensionDTO.save_many(
            universe,
            [
                DimensionDTO(
                    slug="state",
                    value_ordering=ValueOrdering.MANUAL,
                    is_public=False,
                    is_list_filter=True,
                    is_key_dimension=False,
                    is_technical=True,
                    title={
                        "fi": "Tila",
                        "en": "State",
                        "sv": "Status",
                    },
                    choices=[
                        DimensionValueDTO(
                            slug="new",
                            is_technical=True,
                            title={
                                "fi": "Uusi",
                                "en": "New",
                                "sv": "Nytt",
                            },
                            color="Blue",
                        ),
                        DimensionValueDTO(
                            slug="accepted",
                            is_technical=True,
                            title={
                                "fi": "Hyväksytty",
                                "en": "Accepted",
                                "sv": "Godkänt",
                            },
                            color="Green",
                        ),
                        DimensionValueDTO(
                            slug="rejected",
                            is_technical=True,
                            title={
                                "fi": "Hylätty",
                                "en": "Rejected",
                                "sv": "Avvisad",
                            },
                            color="Red",
                        ),
                        DimensionValueDTO(
                            slug="cancelled",
                            is_technical=True,
                            title={
                                "fi": "Peruutettu",
                                "en": "Cancelled",
                                "sv": "Avbruten",
                            },
                            color="Red",
                        ),
                    ],
                )
            ],
        )
