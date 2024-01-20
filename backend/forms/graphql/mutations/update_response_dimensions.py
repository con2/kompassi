import graphene
from graphene.types.generic import GenericScalar

from access.cbac import graphql_check_access

from ...models.field import Field, FieldType
from ...models.survey import Survey
from ...utils.process_form_data import process_form_data
from ..response import FullResponseType


class UpdateResponseDimensions(graphene.Mutation):
    class Arguments:
        event_slug = graphene.String(required=True)
        survey_slug = graphene.String(required=True)
        response_id = graphene.String(required=True)
        form_data = GenericScalar(required=True)

    response = graphene.Field(FullResponseType)

    @staticmethod
    def mutate(
        _root,
        info,
        event_slug: str,
        survey_slug: str,
        response_id: str,
        form_data: dict[str, str | list[str]],
    ):
        """
        Called by the dimensions box submit button in
        frontend/src/app/[locale]/events/[eventSlug]/surveys/[surveySlug]/responses/[responseId]/page.tsx

        Each dimension can be either a SingleSelect or a MultiSelect, depending on whether multiple
        values are allowed (or already associated).
        """

        survey = Survey.objects.get(event__slug=event_slug, slug=survey_slug)
        response = survey.responses.get(id=response_id)

        # TODO bastardization of graphql_check_access, rethink
        graphql_check_access(survey, info, "response", "mutation")

        fields_single = [
            Field(slug=dimension.slug, type=FieldType.SINGLE_SELECT, choices=dimension.get_choices())
            for dimension in survey.dimensions.all()
        ]
        fields_multi = [
            Field(slug=dimension.slug, type=FieldType.MULTI_SELECT, choices=dimension.get_choices())
            for dimension in survey.dimensions.all()
        ]

        values_single, warnings_single = process_form_data(fields_single, form_data)
        if warnings_single:
            raise ValueError(warnings_single)

        values_multi, warnings_multi = process_form_data(fields_multi, form_data)
        if warnings_multi:
            raise ValueError(warnings_multi)

        values = {k: {v} for k, v in values_single.items() if v}
        for k, v in values_multi.items():
            values.setdefault(k, set()).update(v)

        response.set_dimension_values(values)

        return UpdateResponseDimensions(response=response)  # type: ignore
