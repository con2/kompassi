import graphene
from django.db import transaction
from graphene.types.generic import GenericScalar

from kompassi.access.cbac import graphql_check_instance
from kompassi.dimensions.utils.process_dimension_value_selection_form import process_dimension_value_selection_form

from ...models.survey import Survey
from ..response_full import FullResponseType


class UpdateResponseDimensionsInput(graphene.InputObjectType):
    event_slug = graphene.String(required=True)
    survey_slug = graphene.String(required=True)
    response_id = graphene.String(required=True)
    form_data = GenericScalar(required=True)


class UpdateResponseDimensions(graphene.Mutation):
    class Arguments:
        input = UpdateResponseDimensionsInput(required=True)

    response = graphene.Field(FullResponseType)

    @staticmethod
    def mutate(
        _root,
        info,
        input: UpdateResponseDimensionsInput,
    ):
        """
        Called by the dimensions box submit button in
        frontend/src/app/[locale]/events/[eventSlug]/surveys/[surveySlug]/responses/[responseId]/page.tsx

        Each dimension can be either a SingleSelect or a MultiSelect, depending on whether multiple
        values are allowed (or already associated).
        """
        form_data: dict[str, str] = input.form_data  # type: ignore

        survey = Survey.objects.get(event__slug=input.event_slug, slug=input.survey_slug)
        response = survey.current_responses.get(id=input.response_id)

        dimensions = list(survey.dimensions.filter(is_technical=False))

        graphql_check_instance(
            response,
            info,
            app=survey.app_name,
            field="dimensions",
            operation="update",
        )

        values = process_dimension_value_selection_form(dimensions, form_data)
        cache = survey.universe.preload_dimensions(dimension_slugs=values.keys())

        with transaction.atomic():
            response.set_dimension_values(values, cache=cache)
            response.refresh_cached_fields()

        survey.workflow.handle_response_dimension_update(response)

        return UpdateResponseDimensions(response=response)  # type: ignore
