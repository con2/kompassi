import pytest

from kompassi.core.models.event import Event
from kompassi.core.models.person import Person
from kompassi.dimensions.models.annotation_dto import AnnotationDTO
from kompassi.dimensions.models.dimension_dto import DimensionDTO, DimensionValueDTO
from kompassi.dimensions.models.enums import AnnotationDataType
from kompassi.dimensions.models.universe_annotation import UniverseAnnotation

from .emperkelators.desucon2026 import DesuconEmperkelator
from .emperkelators.ropecon2026 import RopeconEmperkelator
from .emperkelators.tracon2025 import TraconEmperkelator
from .models.enums import InvolvementApp, InvolvementType
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


def test_tracon_get_formatted_perks_computed():
    dimension_values = {"ticket-type": ["internal-badge"]}
    annotation_values = {"tracon:mealVouchers": 2, "tracon:swag": True, "tracon:extraSwag": False}

    assert (
        TraconEmperkelator.get_formatted_perks(dimension_values, annotation_values)
        == "Badge (internal), 2 ruokalippua, valittu työvoimatuote"
    )


def test_tracon_get_formatted_perks_no_meals_no_swag():
    dimension_values = {"ticket-type": []}
    annotation_values = {"tracon:mealVouchers": 0, "tracon:swag": False, "tracon:extraSwag": False}

    assert (
        TraconEmperkelator.get_formatted_perks(dimension_values, annotation_values)
        == "Ei lippuetua, ei ruokalippuja, ei työvoimatuotteita"
    )


def test_tracon_get_formatted_perks_extra_swag():
    dimension_values = {"ticket-type": ["super-internal-badge"]}
    annotation_values = {"tracon:mealVouchers": 4, "tracon:swag": True, "tracon:extraSwag": True}

    assert (
        TraconEmperkelator.get_formatted_perks(dimension_values, annotation_values)
        == "Badge (super internal), 4 ruokalippua, valittu työvoimatuote ja ekstrajuomapullo"
    )


def test_tracon_get_formatted_perks_override():
    dimension_values = {"ticket-type": ["internal-badge"]}
    annotation_values = {
        "tracon:mealVouchers": 2,
        "internal:overrideFormattedPerks": "Coniitin kirjekuori, valittu työvoimatuote, ekstrajuomapullo",
    }

    assert (
        TraconEmperkelator.get_formatted_perks(dimension_values, annotation_values)
        == "Coniitin kirjekuori, valittu työvoimatuote, ekstrajuomapullo"
    )


def test_desucon_get_formatted_perks_computed():
    dimension_values = {"shirt-type": ["staff"], "shirt-size": ["m-unisex"]}
    annotation_values = {"tracon:mealVouchers": 1}

    assert (
        DesuconEmperkelator.get_formatted_perks(dimension_values, annotation_values)
        == "STAFF-paita (M Unisex), 1 ruokalippu"
    )


def test_desucon_get_formatted_perks_no_shirt():
    dimension_values = {}
    annotation_values = {"tracon:mealVouchers": 2}

    assert DesuconEmperkelator.get_formatted_perks(dimension_values, annotation_values) == "Ei paitaa, 2 ruokalippua"


def test_desucon_get_formatted_perks_override():
    dimension_values = {"shirt-type": ["staff"], "shirt-size": ["m-unisex"]}
    annotation_values = {"tracon:mealVouchers": 1, "internal:overrideFormattedPerks": "Custom perks"}

    assert DesuconEmperkelator.get_formatted_perks(dimension_values, annotation_values) == "Custom perks"


def test_ropecon_get_formatted_perks_computed():
    dimension_values = {"ticket-type": ["weekend-ticket"], "v1-personnel-class": ["conitea"]}
    annotation_values = {"tracon:mealVouchers": 2}

    assert (
        RopeconEmperkelator.get_formatted_perks(dimension_values, annotation_values)
        == "Viikonloppulippu, coniteabadge, 2\xa0ruokalippua"
    )


def test_ropecon_get_formatted_perks_single_meal():
    dimension_values = {"ticket-type": ["day-ticket"], "v1-personnel-class": ["ohjelma"]}
    annotation_values = {"tracon:mealVouchers": 1}

    assert (
        RopeconEmperkelator.get_formatted_perks(dimension_values, annotation_values)
        == "Päivälippu, ohjelmabadge, 1\xa0ruokalippu"
    )


def test_ropecon_get_formatted_perks_override():
    dimension_values = {"ticket-type": ["day-ticket"]}
    annotation_values = {"tracon:mealVouchers": 1, "internal:overrideFormattedPerks": "Custom override"}

    assert RopeconEmperkelator.get_formatted_perks(dimension_values, annotation_values) == "Custom override"


@pytest.mark.django_db
def test_for_combined_perks_respects_manual_perk_override():
    """
    Regression test: a manually overridden perk must be reflected in the
    internal:formattedPerks stored on the recomputed combined perks involvement,
    not the auto-computed value that TraconEmperkelator would otherwise produce.
    """
    from kompassi.labour.models.labour_event_meta import LabourEventMeta
    from kompassi.labour.models.personnel_class import PersonnelClass

    person, _ = Person.get_or_create_dummy()
    event, _ = Event.get_or_create_dummy(name="Formatted Perks Test 2099")
    event.slug = "tracon2099"
    event.save(update_fields=["slug"])

    # TraconEmperkelator only registers the v1-personnel-class dimension (and the
    # PROGRAM_HOST involvement path hardcodes its value to "ohjelma") if the event
    # has a LabourEventMeta and a matching PersonnelClass.
    LabourEventMeta.get_or_create_dummy(event=event)
    PersonnelClass.objects.create(event=event, name="Ohjelma", slug="ohjelma", app_label="program_v2")

    # ensure() registers the "registry" dimension's values from the scope's existing
    # registries before it creates the default "volunteers" registry, so the first
    # call never has "volunteers" as a choice. Calling it again picks it up.
    InvolvementEventMeta.ensure(event)
    meta = InvolvementEventMeta.ensure(event)
    universe = meta.universe

    # An active involvement so for_combined_perks has something to compute from.
    # Perks.for_program_host always grants INTERNAL_BADGE, regardless of the
    # involvement's program/response.
    Involvement.objects.create(
        universe=universe,
        person=person,
        app=InvolvementApp.PROGRAM,
        type=InvolvementType.PROGRAM_HOST,
        registry=meta.default_registry,
        is_active=True,
    )

    # Existing combined perks with ticket-type manually overridden to a higher tier
    # than what the auto-computation (INTERNAL_BADGE) would produce.
    Involvement.objects.create(
        universe=universe,
        person=person,
        app=InvolvementApp.INVOLVEMENT,
        type=InvolvementType.COMBINED_PERKS,
        registry=meta.default_registry,
        is_active=True,
        cached_dimensions={
            MANUAL_PERKS_OVERRIDE_SLUG: [dimension_override_value("ticket-type")],
            "ticket-type": ["super-internal-badge"],
        },
    )

    result = Involvement.for_combined_perks(event, person)

    assert result is not None
    assert result.cached_dimensions["ticket-type"] == ["super-internal-badge"]

    formatted_perks = result.annotations["internal:formattedPerks"]
    assert "Badge (super internal)" in formatted_perks
    assert "Badge (internal)," not in formatted_perks
