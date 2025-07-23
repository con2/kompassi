from collections import Counter
from functools import reduce

from kompassi.core.utils.model_utils import slugify
from kompassi.dimensions.models.dimension import ValueOrdering
from kompassi.dimensions.models.dimension_dto import DimensionDTO, DimensionValueDTO

from ..models.field import BOOLEAN_CHOICES, BOOLEAN_TRANSLATIONS, Choice, Field, FieldType
from ..models.response import Response
from ..models.survey import Survey
from ..utils.lift_dimension_values import lift_dimension_values
from ..utils.merge_form_fields import merge_choices


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
        case FieldType.SINGLE_SELECT | FieldType.TRISTATE:
            field_type = FieldType.DIMENSION_SINGLE_SELECT
        case FieldType.SINGLE_CHECKBOX:
            field_type = FieldType.DIMENSION_SINGLE_CHECKBOX
        case FieldType.MULTI_SELECT:
            field_type = FieldType.DIMENSION_MULTI_SELECT
        case _:
            raise NotImplementedError(original_field_type)

    choices: list[Choice]
    match original_field_type:
        case FieldType.SINGLE_SELECT | FieldType.MULTI_SELECT:
            # use merge_choices for consistent ordering
            choices = (
                reduce(
                    merge_choices,
                    [field.choices for field in field_in_languages.values()],
                )
                or []
            )
        case FieldType.SINGLE_CHECKBOX | FieldType.TRISTATE:
            choices = BOOLEAN_CHOICES
        case _:
            raise NotImplementedError(original_field_type)

    # convert underscore to hyphen
    dimension_slug = slugify(field_slug)

    # don't want to lose existing translations
    cache = survey.universe.preload_dimensions(
        dimension_slugs=[dimension_slug],
        allow_missing=True,  # we might be creating a new dimension
    )

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
            if original_field_type in (FieldType.SINGLE_CHECKBOX, FieldType.TRISTATE)
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

        form.save()

    # reload cache
    cache = survey.universe.preload_dimensions(dimension_slugs=[dimension_slug])

    # lift values of the field to the dimension in responses
    for form in forms:
        for response in form.all_responses.all():  # NOTE also old versions!
            lift_dimension_values(
                response,
                dimension_slugs=[dimension.slug],
                cache=cache,
            )

    Response.refresh_cached_fields_qs(Response.objects.filter(form__in=forms))
