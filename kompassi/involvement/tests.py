import pytest

from kompassi.dimensions.models.annotation_dto import AnnotationDTO
from kompassi.dimensions.models.dimension_dto import DimensionDTO, DimensionValueDTO
from kompassi.dimensions.models.enums import AnnotationDataType
from kompassi.dimensions.models.universe_annotation import UniverseAnnotation

from .models.involvement import Involvement
from .models.meta import InvolvementEventMeta
from .perks import (
    MANUAL_PERKS_OVERRIDE_SLUG,
    annotation_override_value,
    dimension_override_value,
    get_manual_perks_override_dimension,
    get_perk_keys,
)


@pytest.mark.parametrize(
    "annotation_slug,expected",
    [
        ("tracon:mealVouchers", "a-tracon-meal-vouchers"),
        ("tracon:swag", "a-tracon-swag"),
        ("tracon:extraSwag", "a-tracon-extra-swag"),
        ("internal:overrideBadgeJobTitle", "a-internal-override-badge-job-title"),
    ],
)
def test_annotation_override_value(annotation_slug: str, expected: str):
    assert annotation_override_value(annotation_slug) == expected


def test_dimension_override_value():
    assert dimension_override_value("ticket-type") == "d-ticket-type"


def _setup_perk_universe():
    """Set up a dummy involvement universe with one dimension perk and one annotation perk."""
    meta, _ = InvolvementEventMeta.get_or_create_dummy()
    universe = meta.universe

    DimensionDTO(
        slug="ticket-type",
        title=dict(en="Ticket type"),
        choices=[
            DimensionValueDTO(slug="basic", title=dict(en="Basic")),
            DimensionValueDTO(slug="vip", title=dict(en="VIP")),
        ],
    ).save(universe)

    annotations = AnnotationDTO.save_many(
        [
            AnnotationDTO(
                slug="tracon:mealVouchers",
                title=dict(en="Meal vouchers"),
                type=AnnotationDataType.NUMBER,
                is_perk=True,
                is_applicable_to_involvements=True,
                is_applicable_to_program_items=False,
            )
        ]
    )
    UniverseAnnotation.ensure(universe, annotations)

    get_manual_perks_override_dimension().save(universe)

    return universe


@pytest.mark.django_db
def test_get_perk_keys():
    universe = _setup_perk_universe()

    perk_keys = get_perk_keys(universe)

    assert perk_keys["d-ticket-type"].kind == "dimension"
    assert perk_keys["d-ticket-type"].slug == "ticket-type"
    assert perk_keys["a-tracon-meal-vouchers"].kind == "annotation"
    assert perk_keys["a-tracon-meal-vouchers"].slug == "tracon:mealVouchers"

    # technical dimensions are not perks
    assert "d-app" not in perk_keys
    assert "d-type" not in perk_keys
    assert f"d-{MANUAL_PERKS_OVERRIDE_SLUG}" not in perk_keys


@pytest.mark.django_db
def test_preserve_manual_perk_overrides():
    universe = _setup_perk_universe()

    existing = Involvement(
        cached_dimensions={
            MANUAL_PERKS_OVERRIDE_SLUG: ["d-ticket-type", "a-tracon-meal-vouchers"],
            "ticket-type": ["vip"],
        },
        annotations={"tracon:mealVouchers": 3},
    )

    # Automatically computed values that should be overridden by the manual ones.
    dimension_values = {"ticket-type": ["basic"]}
    annotation_values = {"tracon:mealVouchers": 1, "internal:formattedPerks": "auto"}

    Involvement._preserve_manual_perk_overrides(universe, existing, dimension_values, annotation_values)

    assert dimension_values["ticket-type"] == ["vip"]
    assert annotation_values["tracon:mealVouchers"] == 3
    # non-overridden computed values are left untouched
    assert annotation_values["internal:formattedPerks"] == "auto"


@pytest.mark.django_db
def test_non_overridden_perks_are_not_preserved():
    universe = _setup_perk_universe()

    existing = Involvement(
        cached_dimensions={MANUAL_PERKS_OVERRIDE_SLUG: [], "ticket-type": ["vip"]},
        annotations={"tracon:mealVouchers": 3},
    )

    dimension_values = {"ticket-type": ["basic"]}
    annotation_values = {"tracon:mealVouchers": 1}

    Involvement._preserve_manual_perk_overrides(universe, existing, dimension_values, annotation_values)

    # With no overrides recorded, the automatically computed values stand.
    assert dimension_values["ticket-type"] == ["basic"]
    assert annotation_values["tracon:mealVouchers"] == 1
