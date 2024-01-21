import graphene
from graphene.types.generic import GenericScalar

from access.cbac import graphql_check_access

from ...models.field import Field, FieldType
from ...models.survey import Survey
from ...utils.process_form_data import process_form_data
from ..response import FullResponseType


class UpdateResponseDimensionsInput(graphene.InputObjectType):
    event_slug = graphene.String(required=True)
    survey_slug = graphene.String(required=True)
    response_id = graphene.String(required=True)
    form_data = GenericScalar(required=True)


SENTINEL_BYPASS_PERMISSION_CHECK_FOR_TESTING = object()


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

        # TODO bastardization of graphql_check_access, rethink
        if info is not SENTINEL_BYPASS_PERMISSION_CHECK_FOR_TESTING:
            graphql_check_access(survey, info, "response", "mutation")

        fields_single = [Field.from_dimension(dimension, FieldType.SINGLE_SELECT) for dimension in dimensions]
        fields_multi = [Field.from_dimension(dimension, FieldType.MULTI_SELECT) for dimension in dimensions]

        values_single, warnings_single = process_form_data(fields_single, form_data)
        if warnings_single:
            raise ValueError(warnings_single)

        values_multi, warnings_multi = process_form_data(fields_multi, form_data)
        if warnings_multi:
            raise ValueError(warnings_multi)

        values: dict[str, list[str]] = {k: [v] for k, v in values_single.items() if v}
        for k, v in values_multi.items():
            values.setdefault(k, []).extend(v)

        response.set_dimension_values(values)

        return UpdateResponseDimensions(response=response)  # type: ignore
