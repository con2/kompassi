from __future__ import annotations

from typing import TYPE_CHECKING

from kompassi.dimensions.models.dimension_dto import DimensionDTO, DimensionValueDTO, ValueOrdering

if TYPE_CHECKING:
    from kompassi.program_v2.models.program import Program


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
            # note: camelCase slugs defined by Konsti, pending discussion for consistency in later events
            ("tabletopRPG", "Pöytäroolipeli", "Tabletop RPG"),
            ("larp", "Larppi", "LARP"),
            ("tournament", "Turnaus", "Tournament"),
            ("workshop", "Työpaja", "Workshop"),
            ("experiencePoint", "Kokemuspiste", "Experience Point"),
            ("other", "Muu", "Other"),
            ("fleamarket", "Kirpputori", "Flea market"),
        ]
    ],
)


def get_konsti_signup_url(program: Program) -> str:
    """
    Returns the Konsti signup URL for this program if it is set up for Konsti
    and has a single schedule item. It will be put in the `internal:links:signup` annotation.

    TODO(#801) Should be separately on each schedule item
    """
    if not (
        # is already saved (cannot have annotations or dimensions otherwise)
        program.pk
        # the event is set up for Konsti
        and program.meta.konsti_url
        # this event is using Konsti
        and program.cached_dimensions.get("konsti", "")
        # this program is not a placeholder in Konsti
        and not program.annotations.get("konsti:isPlaceholder", False)
        # it has exactly one schedule item to determine the slug in Konsti
        and program.schedule_items.count() == 1
    ):
        return ""

    sole_schedule_item = program.schedule_items.get()
    return f"{program.meta.konsti_url}/program/item/{sole_schedule_item.slug}"
