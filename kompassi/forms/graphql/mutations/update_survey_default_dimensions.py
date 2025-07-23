from enum import Enum

import graphene
from django.db import transaction
from graphene.types.generic import GenericScalar

from kompassi.access.cbac import graphql_check_instance
from kompassi.dimensions.utils.process_dimension_value_selection_form import process_dimension_value_selection_form

from ...models.survey import Survey
from ..survey_full import FullSurveyType


class SurveyDefaultDimensionsUniverse(Enum):
    RESPONSE = "response"
    INVOLVEMENT = "involvement"


SurveyDefaultDimensionsUniverseType = graphene.Enum.from_enum(SurveyDefaultDimensionsUniverse)


class UpdateSurveyDefaultDimensionsInput(graphene.InputObjectType):
    event_slug = graphene.String(required=True)
    survey_slug = graphene.String(required=True)
    form_data = GenericScalar(required=True)
    universe = graphene.Field(SurveyDefaultDimensionsUniverseType, required=True)


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

        graphql_check_instance(
            survey,
            info,
            app=survey.app.value,
            field="default_dimensions",
            operation="update",
        )

        match input.universe:
            case SurveyDefaultDimensionsUniverse.RESPONSE:
                universe = survey.universe
            case SurveyDefaultDimensionsUniverse.INVOLVEMENT:
                universe = survey.event.involvement_universe
            case _:
                raise ValueError(f"Invalid universe: {input.universe}")

        dimensions = list(universe.dimensions.filter(is_technical=False))
        values = process_dimension_value_selection_form(dimensions, form_data)
        cache = universe.preload_dimensions(dimension_slugs=values.keys())

        with transaction.atomic():
            match input.universe:
                case SurveyDefaultDimensionsUniverse.RESPONSE:
                    survey.set_default_response_dimension_values(values, cache)
                case SurveyDefaultDimensionsUniverse.INVOLVEMENT:
                    survey.set_default_involvement_dimension_values(values, cache)
                case _:
                    raise AssertionError("We should never get here")

            survey.refresh_cached_default_dimensions()

        return UpdateSurveyDefaultDimensions(survey=survey)  # type: ignore
