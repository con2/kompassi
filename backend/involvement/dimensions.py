from __future__ import annotations

from core.models.event import Event
from dimensions.models.dimension_dto import DimensionDTO
from dimensions.models.dimension_value_dto import DimensionValueDTO
from dimensions.models.enums import DimensionApp
from dimensions.models.universe import Universe

from .models.enums import InvolvementApp

# NOTE SUPPORTED_LANGUAGES
DIMENSIONS = [
    DimensionDTO(
        slug="app",
        title=dict(
            en="App",
            fi="Sovellus",
            sv="App",
        ),
        is_technical=True,
        order=-9100,
        choices=[
            DimensionValueDTO(
                slug=app.value,
                title=dict(en=app.label),
                is_technical=True,
            )
            for app in InvolvementApp
        ],
    ),
    DimensionDTO(
        slug="type",
        title=dict(
            en="Type",
            fi="Tyyppi",
            sv="Typ",
        ),
        is_technical=True,
        order=-9000,
        choices=[
            DimensionValueDTO(
                slug="program-offer",
                title=dict(
                    en="Program offer",
                    fi="Ohjelmatarjous",
                ),
                is_technical=True,
            ),
            DimensionValueDTO(
                slug="program-host",
                title=dict(
                    en="Program host",
                    fi="Ohjelmanumero",
                ),
                is_technical=True,
            ),
        ],
    ),
    DimensionDTO(
        slug="state",
        title=dict(
            en="State",
            fi="Tila",
            sv="Status",
        ),
        is_technical=True,
        order=9000,
        choices=[
            DimensionValueDTO(
                slug="active",
                title=dict(
                    en="Active",
                    fi="Aktiivinen",
                    sv="Aktiv",
                ),
                is_technical=True,
            ),
            DimensionValueDTO(
                slug="inactive",
                title=dict(
                    en="Inactive",
                    fi="Ei aktiivinen",
                    sv="Inaktiv",
                ),
                is_technical=True,
            ),
        ],
    ),
]


def get_involvement_universe(event: Event) -> Universe:
    universe, created = Universe.objects.get_or_create(
        scope=event.scope,
        slug="involvement",
        app_name=DimensionApp.INVOLVEMENT.value,
    )

    if created:
        setup_involvement_dimensions(universe)

    return universe


def setup_involvement_dimensions(universe: Universe) -> None:
    DimensionDTO.save_many(universe, DIMENSIONS, override_order=True)
