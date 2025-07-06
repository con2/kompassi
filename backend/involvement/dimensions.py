from __future__ import annotations

from core.models.event import Event
from dimensions.models.dimension_dto import DimensionDTO
from dimensions.models.dimension_value_dto import DimensionValueDTO
from dimensions.models.enums import DimensionApp
from dimensions.models.universe import Universe

from .models.enums import InvolvementApp, InvolvementType

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
                title=app.get_title_dict(),
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
                slug=type.value,
                title=type.get_title_dict(),
                is_technical=True,
            )
            for type in InvolvementType
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


def get_registry_dimension(event: Event) -> DimensionDTO:
    return DimensionDTO(
        slug="registry",
        title=dict(
            en="Registry",
            fi="Rekisteri",
            sv="Register",
        ),
        is_technical=True,
        order=-9200,
        choices=[
            DimensionValueDTO(
                slug=registry.slug,
                title=registry.get_title_dict(),
                is_technical=True,
            )
            for registry in event.organization.scope.registries.all()
        ],
    )


def get_involvement_universe(event: Event) -> Universe:
    universe, created = Universe.objects.get_or_create(
        scope=event.scope,
        slug="involvement",
        app_name=DimensionApp.INVOLVEMENT.value,
    )

    if created:
        setup_involvement_dimensions(universe, event)

    return universe


def setup_involvement_dimensions(universe: Universe, event: Event) -> None:
    dimensions = [
        *DIMENSIONS,
        get_registry_dimension(event),
    ]
    DimensionDTO.save_many(universe, dimensions, override_order=True)
