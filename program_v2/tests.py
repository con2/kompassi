import pytest

from core.models import Event

from .models import Program, Dimension, DimensionValue


@pytest.mark.django_db
def test_program_from_form_data():
    event, _ = Event.get_or_create_dummy()

    category_dimension = Dimension.objects.create(
        event=event,
        slug="category",
        title=dict(fi="Kategoria", en="Category"),
    )

    for category_slug, category_title_fi, category_title_en in [
        ("anime", "Animeohjelma", "Anime program"),
        ("kender", "Kenttiongelma", "Kender problem"),
    ]:
        DimensionValue.objects.create(
            dimension=category_dimension,
            slug=category_slug,
            title=dict(fi=category_title_fi, en=category_title_en),
        )

    data = dict(
        title="Ei kenttiongelmaa",
        description="Ropeconissa ei ole kenttiongelmaa",
        category="kender",
        this_field_should_be_in="other_fields",
    )

    program = Program.create_from_form_data(event, data)

    assert program.title == "Ei kenttiongelmaa"
    assert program.description == "Ropeconissa ei ole kenttiongelmaa"
    assert program.cached_dimensions == dict(category=["kender"])
    assert program.other_fields == dict(
        this_field_should_be_in="other_fields",
    )

    program = program.update_from_form_data(
        dict(
            title="Kenttiongelma",
            description="Ropeconissa on kenttiongelma",
            category="anime",
            this_field_should_be_in="other_fields",
            also_this_field_should_be_in="other_fields2",
        )
    )

    assert program.title == "Kenttiongelma"
    assert program.description == "Ropeconissa on kenttiongelma"
    assert program.cached_dimensions == dict(category=["anime"])
    assert program.other_fields == dict(
        this_field_should_be_in="other_fields",
        also_this_field_should_be_in="other_fields2",
    )
