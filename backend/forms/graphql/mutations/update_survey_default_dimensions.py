import graphene
from django.db import transaction
from graphene.types.generic import GenericScalar

from access.cbac import graphql_check_instance
from dimensions.utils.process_dimension_value_selection_form import process_dimension_value_selection_form

from ...models.survey import Survey
from ..survey_full import FullSurveyType


class UpdateSurveyDefaultDimensionsInput(graphene.InputObjectType):
    event_slug = graphene.String(required=True)
    survey_slug = graphene.String(required=True)
    form_data = GenericScalar(required=True)


class UpdateSurveyDefaultDimensions(graphene.Mutation):
    class Arguments:
        input = UpdateSurveyDefaultDimensionsInput(required=True)

    survey = graphene.Field(FullSurveyType)

    @staticmethod
    def mutate(
        _root,
        info,
        input: UpdateSurveyDefaultDimensionsInput,
    ):
        form_data: dict[str, str] = input.form_data  # type: ignore

        survey = Survey.objects.get(event__slug=input.event_slug, slug=input.survey_slug)
        dimensions = list(survey.dimensions.filter(is_technical=False))

        graphql_check_instance(
            survey,
            info,
            app=survey.app_name,
            field="default_dimensions",
            operation="update",
        )

        values = process_dimension_value_selection_form(dimensions, form_data)
        cache = survey.universe.preload_dimensions(dimension_slugs=values.keys())

        with transaction.atomic():
            survey.set_default_response_dimension_values(values, cache)
            survey.refresh_cached_default_dimensions()

        return UpdateSurveyDefaultDimensions(survey=survey)  # type: ignore
