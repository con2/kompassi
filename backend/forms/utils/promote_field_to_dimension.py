from collections import Counter
from functools import reduce

from core.utils.model_utils import slugify
from dimensions.models.dimension import ValueOrdering
from dimensions.models.dimension_dto import DimensionDTO, DimensionValueDTO

from ..models.field import Choice, Field, FieldType
from ..models.form import Form
from ..models.response import Response
from ..models.survey import Survey
from ..utils.lift_dimension_values import lift_dimension_values
from ..utils.merge_form_fields import merge_choices

BOOLEAN_CHOICES = [
    Choice(slug="true"),
    Choice(slug="false"),
]
BOOLEAN_TRANSLATIONS = {
    "true": {
        "en": "Yes",
        "fi": "Kyllä",
        "sv": "Ja",
    },
    "false": {
        "en": "No",
        "fi": "Ei",
        "sv": "Nej",
    },
}


def promote_field_to_dimension(survey: Survey, field_slug: str):
    """
    Converts a field in the survey to a dimension.

    XXX Here be dragons.
    """

    forms = list(survey.languages.all())

    field_in_languages: dict[str, Field] = {
        form.language: field
        for form in forms
        for field in form.validated_fields
        if field.slug == field_slug and field.type.is_convertible_to_dimension
    }

    if not field_in_languages:
        raise KeyError(f"Did not find a dimension-convertible field {field_slug} in any of the languages.")

    # make the language versions vote for the field type
    original_field_type = Counter(field.type for field in field_in_languages.values()).most_common(1)[0][0]
    match original_field_type:
        case FieldType.SINGLE_SELECT:
            field_type = FieldType.DIMENSION_SINGLE_SELECT
        case FieldType.SINGLE_CHECKBOX:
            field_type = FieldType.DIMENSION_SINGLE_CHECKBOX
        case FieldType.MULTI_SELECT:
            field_type = FieldType.DIMENSION_MULTI_SELECT
        case _:
            raise NotImplementedError(original_field_type)

    # use merge_choices for consistent ordering
    choices = (
        BOOLEAN_CHOICES
        if original_field_type == FieldType.SINGLE_CHECKBOX
        else (
            reduce(
                merge_choices,
                [field.choices for field in field_in_languages.values()],
            )
            or []
        )
    )

    # convert underscore to hyphen
    dimension_slug = slugify(field_slug)

    # don't want to lose existing translations
    cache = survey.universe.preload_dimensions(dimension_slugs=[dimension_slug])

    def merge_choice_translations(choice_slug: str) -> dict[str, str]:
        value = cache.values_by_dimension.get(dimension_slug, {}).get(slugify(choice_slug))
        title_dict = dict(value.title_dict) if value else {}

        for language, field in field_in_languages.items():
            for choice in field.choices or []:
                if choice.slug == choice_slug:
                    title_dict[language] = choice.title

        return title_dict

    # gather translations for choices
    value_dtos = [
        DimensionValueDTO(
            slug=slugify(choice.slug),
            title=BOOLEAN_TRANSLATIONS[choice.slug]
            if original_field_type == FieldType.SINGLE_CHECKBOX
            else merge_choice_translations(choice.slug),
        )
        for choice in choices
    ]

    # gather translations for the dimension
    dimension = cache.dimensions.get(dimension_slug)
    title_dict: dict[str, str] = dict(dimension.title_dict) if dimension else {}
    for language, field in field_in_languages.items():
        if field.title:
            title_dict[language] = field.title

    dimension = DimensionDTO(
        slug=dimension_slug,
        title=title_dict,
        choices=value_dtos,
        value_ordering=ValueOrdering.MANUAL,
    ).save(survey.universe)

    # replace the field in all languages with a dimension field
    for form in forms:
        original_field = field_in_languages.get(form.language)
        if not original_field:
            # this language does not have the field
            continue

        form.replace_field(
            field_slug,
            Field(
                slug=field_slug,
                type=field_type,
                dimension=dimension.slug,
                title=original_field.title,
                required=original_field.required,
                subset_values=[choice.slug for choice in original_field.choices] if original_field.choices else None,
            ),
        )

    Form.objects.bulk_update(forms, ["fields", "cached_enriched_fields"])
    Form.refresh_enriched_fields_qs(Form.objects.filter(id__in=[form.id for form in forms]))

    # reload cache
    cache = survey.universe.preload_dimensions(dimension_slugs=[dimension_slug])

    # lift values of the field to the dimension in responses
    bulk_update = []
    for form in forms:
        for response in form.responses.all():
            response.reslugify_field(field_slug, "-")  # dimensions use dashes due to being parts of URLs
            lift_dimension_values(
                response,
                dimension_slugs=[dimension.slug],
                cache=cache,
            )

    Response.objects.bulk_update(bulk_update, ["form_data"])
    Response.refresh_cached_fields_qs(Response.objects.filter(form__in=forms))
