import logging
from collections.abc import Iterable, Sequence
from datetime import timedelta

from kompassi.core.models.event import Event
from kompassi.dimensions.models.dimension import Dimension
from kompassi.dimensions.models.dimension_dto import DimensionDTO, DimensionValueDTO, ValueOrdering
from kompassi.dimensions.models.enums import DimensionApp
from kompassi.dimensions.models.universe import Universe
from kompassi.graphql_api.language import SUPPORTED_LANGUAGE_CODES

logger = logging.getLogger(__name__)

DATE_DIMENSION_TITLE_LOCALIZED = dict(
    fi="Päivä",
    en="Day",
    sv="Dag",
)

ROOM_DIMENSION_DTO = DimensionDTO(
    slug="room",
    value_ordering=ValueOrdering.TITLE,
    is_public=True,
    is_list_filter=True,
    is_key_dimension=False,
    is_technical=True,
    can_values_be_added=True,
    title=dict(
        fi="Sali",
        en="Room",
        sv="Sal",
    ),
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
    can_values_be_added=False,
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
            # cannot use is_subject_locked on state=accepted because
            # we may want to allow editing the program but not the offer
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
            is_subject_locked=True,
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
            is_subject_locked=True,
            title={
                "fi": "Peruutettu",
                "en": "Cancelled",
                "sv": "Avbruten",
            },
            color="Red",
        ),
    ],
)

SCHEDULED_DIMENSION_DTO = DimensionDTO(
    slug="scheduled",
    value_ordering=ValueOrdering.MANUAL,
    # applies_to=DimensionAppliesTo.PROGRAM_ITEM,
    is_technical=True,
    can_values_be_added=False,
    is_public=False,
    is_list_filter=True,
    is_key_dimension=False,  # column added manually in program item list view
    is_multi_value=True,
    title=dict(
        fi="Aikataulutettu",
        en="Scheduled",
    ),
    choices=[
        DimensionValueDTO(
            slug="none",
            is_technical=True,
            title={
                "fi": "Ei aikataulutettu",
                "en": "Not yet scheduled",
            },
        ),
        DimensionValueDTO(
            slug="one",
            is_technical=True,
            title={
                "fi": "Yksi aikataulumerkintä",
                "en": "One schedule item",
            },
        ),
        DimensionValueDTO(
            slug="one-or-more",
            is_technical=True,
            title={
                "fi": "Yksi tai useampia aikataulumerkintöjä",
                "en": "One or more schedule items",
            },
        ),
        DimensionValueDTO(
            slug="multiple",
            is_technical=True,
            title={
                "fi": "Useita aikataulumerkintöjä",
                "en": "Multiple schedule items",
            },
        ),
    ],
)


def get_scheduled_dimension_value(count_schedule_items: int) -> list[str]:
    match count_schedule_items:
        case 0:
            return ["none"]
        case 1:
            return ["one", "one-or-more"]
        case _ if count_schedule_items > 1:
            return ["one-or-more", "multiple"]
        case _:
            raise ValueError(f"Invalid count_schedule_items: {count_schedule_items}. Must be >= 0.")


def get_program_universe(event: Event) -> Universe:
    """
    Returns the universe for the program offer workflow.
    """
    universe, created = Universe.objects.get_or_create(
        scope=event.scope,
        slug="program",
        app_name=DimensionApp.PROGRAM_V2.value,
    )

    if created:
        setup_program_dimensions(universe)

    return universe


def setup_program_dimensions(universe: Universe) -> Sequence[Dimension]:
    from .integrations.konsti import KONSTI_DIMENSION_DTO
    from .integrations.paikkala_integration import get_paikkala_dimension

    dimension_dtos = [
        # date dimension before user specified dimensions
        get_date_dimension_dto(universe).model_copy(update=dict(order=-9000)),
        # other technical dimensions after user specified dimensions
        ROOM_DIMENSION_DTO.model_copy(update=dict(order=9000)),
        get_form_dimension_dto(universe).model_copy(update=dict(order=9100)),
        KONSTI_DIMENSION_DTO.model_copy(update=dict(order=9150)),
        STATE_DIMENSION_DTO.model_copy(update=dict(order=9200)),
        SCHEDULED_DIMENSION_DTO.model_copy(update=dict(order=9300)),
    ]

    if (event := universe.scope.event) and (paikkala_dimension := get_paikkala_dimension(event)):
        dimension_dtos.append(paikkala_dimension.model_copy(update=dict(order=9160)))

    return DimensionDTO.save_many(universe, dimension_dtos)


def get_form_dimension_dto(universe: Universe) -> DimensionDTO:
    """
    We make the form used to submit a program offer a dimension
    in order to not have to build separate filters for it.
    """
    event = universe.scope.event
    if event is None:
        raise ValueError("Program universe scope has no event")

    meta = event.program_v2_event_meta
    if meta is None:
        raise ValueError("Event has no program_v2_event_meta")

    return DimensionDTO(
        slug="form",
        value_ordering=ValueOrdering.TITLE,
        is_public=False,
        is_list_filter=True,
        is_key_dimension=True,
        is_technical=True,
        can_values_be_added=False,
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
            for survey in meta.program_offer_forms.only("id", "slug")
        ],
    )


def get_date_dimension_values(universe: Universe) -> Iterable[DimensionValueDTO]:
    """
    Return a list of DimensionValueDTOs for the date dimension.
    """
    event = universe.scope.event
    if event is None:
        raise ValueError("Program universe scope has no event")

    tz = event.timezone

    if not event.start_time:
        raise ValueError(f"Event {event} has no start time")
    if not event.end_time:
        raise ValueError(f"Event {event} has no end time")

    cur_date = event.start_time.astimezone(tz).date()
    end_date = event.end_time.astimezone(tz).date()

    while cur_date <= end_date:
        yield DimensionValueDTO(
            slug=cur_date.isoformat(),
            title={
                lang_code: WEEKDAYS_LOCALIZED[lang_code][cur_date.weekday()] for lang_code in SUPPORTED_LANGUAGE_CODES
            },
            is_technical=True,
        )
        cur_date += timedelta(days=1)


def get_date_dimension_dto(universe: Universe) -> DimensionDTO:
    return DimensionDTO(
        slug="date",
        title=DATE_DIMENSION_TITLE_LOCALIZED,
        choices=list(get_date_dimension_values(universe)),
        order=-9000,
        value_ordering=ValueOrdering.SLUG,
        is_public=True,
        is_list_filter=True,
        is_technical=True,
        can_values_be_added=False,
        is_multi_value=True,
    )
