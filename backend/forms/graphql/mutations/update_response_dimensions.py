import graphene
from graphene.types.generic import GenericScalar

from access.cbac import graphql_check_instance
from dimensions.utils.process_dimensions_form import process_dimensions_form

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
        response = survey.responses.get(id=input.response_id)
        dimensions = list(survey.dimensions.all())

        graphql_check_instance(
            response,
            info,
            app=survey.app,
            field="dimensions",
            operation="update",
        )

        values = process_dimensions_form(dimensions, form_data)
        response.set_dimension_values(values)

        return UpdateResponseDimensions(response=response)  # type: ignore
