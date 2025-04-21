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

DATE_DIMENSION_TITLE_LOCALIZED = dict(
    fi="Päivä",
    en="Day",
    sv="Dag",
)

ROOM_DIMENSION_TITLE_LOCALIZED = dict(
    fi="Sali",
    en="Room",
    sv="Sal",
)

WEEKDAYS_LOCALIZED = dict(
    fi=["maanantai", "tiistai", "keskiviikko", "torstai", "perjantai", "lauantai", "sunnuntai"],
    en=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
    sv=["måndag", "tisdag", "onsdag", "torsdag", "fredag", "lördag", "söndag"],
)


STATE_DIMENSION_DTO = DimensionDTO(
    slug="state",
    value_ordering=ValueOrdering.MANUAL,
    is_public=False,
    is_list_filter=True,
    is_key_dimension=True,
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


class ProgramOfferWorkflow(Workflow, arbitrary_types_allowed=True):
    """
    Workflow for program offers. This workflow is used to set the state of the program offer
    and possibly other automated actions in the future.
    """

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
            values = dict(
                state=["accepted"] if program_offer.programs.exists() else ["new"],
                form=[program_offer.survey.slug],
            )
            program_offer.set_dimension_values(values)

        for program in Program.objects.filter(event=event):
            values = dict(
                state=["accepted"],
                form=[program.program_offer.survey.slug] if program.program_offer else [],
            )
            program.set_dimension_values({"state": ["accepted"]})

        Program.refresh_cached_dimensions_qs(Program.objects.filter(event=event))

    def handle_form_update(self):
        universe = self.survey.universe
        self._get_form_dimension_dto(universe).save(universe)

    def handle_new_response(self, response: Response):
        """
        Called when a new response is created.
        """
        super().handle_new_response(response)

        values = dict(
            state=["accepted"] if response.programs.exists() else ["new"],
            form=[response.survey.slug],
        )
        response.set_dimension_values(values)

    @classmethod
    def _setup_default_dimensions(cls, universe: Universe) -> Sequence[Dimension]:
        return DimensionDTO.save_many(
            universe,
            [
                cls._get_form_dimension_dto(universe),
                STATE_DIMENSION_DTO,
            ],
        )

    @classmethod
    def _get_form_dimension_dto(cls, universe: Universe) -> DimensionDTO:
        """
        We make the form used to submit a program offer a dimension
        in order to not have to build separate filters for it.
        """
        event = universe.scope.event
        if not event:
            raise ValueError("Event is not set for universe")

        return DimensionDTO(
            slug="form",
            value_ordering=ValueOrdering.TITLE,
            is_public=False,
            is_list_filter=True,
            is_key_dimension=True,
            is_technical=True,
            title={
                "fi": "Ohjelmalomake",
                "en": "Program form",
                "sv": "Programblankett",
            },
            choices=[
                DimensionValueDTO(
                    slug=survey.slug,
                    is_technical=True,
                    title=survey.title_dict,
                )
                for survey in Survey.objects.filter(
                    event=event,
                    app="program_v2",
                ).only("id", "slug")
            ],
        )
