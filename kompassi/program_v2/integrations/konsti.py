from __future__ import annotations

from typing import TYPE_CHECKING

from kompassi.dimensions.models.annotation_dto import AnnotationDTO
from kompassi.dimensions.models.dimension_dto import DimensionDTO, DimensionValueDTO, ValueOrdering
from kompassi.dimensions.models.enums import AnnotationDataType

if TYPE_CHECKING:
    from kompassi.program_v2.models.program import ScheduleItem


def UNSURE(x: str) -> str:
    """
    This function is used to mark machine translated or otherwise uncertain strings
    for review by a professional translator.
    """
    return x


KONSTI_DIMENSION_DTO = DimensionDTO(
    slug="konsti",
    is_list_filter=False,
    is_shown_in_detail=False,
    title=dict(
        fi="Konsti-ilmoittautumistyyppi",
        en="Konsti signup type",
        sv="Konsti-anmälningstyp",
    ),
    value_ordering=ValueOrdering.MANUAL,
    choices=[
        DimensionValueDTO(
            slug=slug,
            title=dict(
                fi=title_fi,
                en=title_en,
            ),
        )
        for slug, title_fi, title_en in [
            ("tabletoprpg", "Pöytäroolipeli", "Tabletop RPG"),
            ("larp", "Larppi", "LARP"),
            ("tournament", "Turnaus", "Tournament"),
            ("workshop", "Työpaja", "Workshop"),
            ("experiencepoint", "Kokemuspiste", "Experience Point"),
            ("other", "Muu", "Other"),
            ("fleamarket", "Kirpputori", "Flea market"),
        ]
    ],
)

KONSTI_ANNOTATION_DTOS = [
    AnnotationDTO(
        slug="konsti:rpgSystem",
        title=dict(
            fi="Pelisysteemi",
            en="RPG system",
            sv="Rollspelssystem",
        ),
    ),
    AnnotationDTO(
        slug="konsti:minAttendance",
        title=dict(
            fi="Minimiosallistujamäärä",
            en="Minimum attendance",
            sv="Minsta antal deltagare",
        ),
        type=AnnotationDataType.NUMBER,
    ),
    AnnotationDTO(
        slug="konsti:maxAttendance",
        title=dict(
            fi="Maksimiosallistujamäärä",
            en="Maximum attendance",
            sv="Högsta antal deltagare",
        ),
        type=AnnotationDataType.NUMBER,
    ),
    AnnotationDTO(
        slug="konsti:isPlaceholder",
        type=AnnotationDataType.BOOLEAN,
        is_shown_in_detail=False,
        title=dict(
            fi="Näytetään Konstissa ilman ilmoittautumista",
            en="Shown in Konsti without signup",
            sv="Visas i Konsti utan anmälan",
        ),
        description=dict(
            en=(
                "If set, the program item will be shown in Konsti without signup. "
                "This is useful to communicate to visitors that are looking for "
                "programs of a type that often uses Konsti signup that "
                "this program exists but does not require signup."
            ),
            fi=(
                "Jos tämä on valittuna ohjelmanumerolle, se näytetään Konstissa siten, "
                "että siihen ei voi ilmoittautua. Tämä on hyödyllistä, jos haluat viestiä "
                "vieraille, että tällainen ohjelma on olemassa, mutta siihen ei tarvitse ilmoittautua tai "
                "ilmoittautuminen on hoidettu jotain muuta kautta."
            ),
        ),
    ),
    AnnotationDTO(
        slug="konsti:workshopFee",
        title=dict(
            fi="Työpajamaksu",
            en="Workshop fee",
            sv="Workshopavgift",
        ),
    ),
    AnnotationDTO(
        slug="konsti:entryConditionK16",
        type=AnnotationDataType.BOOLEAN,
        is_shown_in_detail=False,
        title=dict(
            fi="Ikäraja 16 vuotta",
            en="Age limit 16 years",
            sv="Åldersgräns 16 år",
        ),
        description=dict(
            en=(
                "If set, Konsti will display a warning stating that the program has an age limit of 16 years "
                "due to heavy content. The user will be required to acknowledge this and confirm they are of "
                "required age before proceeding."
            ),
            fi=(
                "Jos tämä on valittuna ohjelmanumerolle, Konsti näyttää ohjelmanumeron yhteydessä varoituksen, "
                "jossa kerrotaan, että ohjelmalla on 16 vuoden ikäraja raskaan sisällön vuoksi. Käyttäjän on "
                "vahvistettava, että hän on vaaditun ikäinen, ennen kuin hän voi ilmoittautua ohjelmanumeroon."
            ),
            sv=UNSURE(
                "Om detta är valt för programnumret kommer Konsti att visa en varning i samband med programnumret, "
                "som anger att programmet har en åldersgräns på 16 år på grund av tungt innehåll. Användaren måste "
                "bekräfta att de är av erforderlig ålder innan de kan anmäla sig till programnumret."
            ),
        ),
    ),
]


DEFAULT_KONSTI_URL = "https://ropekonsti.fi"


def get_konsti_signup_url(schedule_item: ScheduleItem) -> str:
    """
    Returns the Konsti signup URL for this schedule item if it is set up for Konsti.
    """
    meta = schedule_item.meta
    konsti_base_url = meta.konsti_url or DEFAULT_KONSTI_URL

    if not (
        # is already saved (cannot have annotations or dimensions otherwise)
        schedule_item.pk
        # this event is using Konsti
        and schedule_item.program.cached_dimensions.get("konsti", "")
        # this program is not a placeholder in Konsti
        and not schedule_item.program.annotations.get("konsti:isPlaceholder", False)
    ):
        return ""

    return f"{konsti_base_url}/program/item/{schedule_item.slug}"
