from dimensions.models.dimension_dto import DimensionDTO, DimensionValueDTO, ValueOrdering

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
