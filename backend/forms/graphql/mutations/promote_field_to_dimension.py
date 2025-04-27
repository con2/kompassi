import graphene
from django.db import transaction

from access.cbac import graphql_check_instance

from ...models.survey import Survey
from ...utils.promote_field_to_dimension import promote_field_to_dimension
from ..survey_full import FullSurveyType


class PromoteFieldToDimensionInput(graphene.InputObjectType):
    event_slug = graphene.String(required=True)
    survey_slug = graphene.String(required=True)
    field_slug = graphene.String(required=True)


class PromoteFieldToDimension(graphene.Mutation):
    """
    Promotes a Single Select or Multiple Select field to a dimension.

    This is used when a field is created as a Single Select or Multiple Select
    and later discovered that it should be a dimension.
    """

    class Arguments:
        input = PromoteFieldToDimensionInput(required=True)

    survey = graphene.Field(FullSurveyType)

    @transaction.atomic
    @staticmethod
    def mutate(
        root,
        info,
        input: PromoteFieldToDimensionInput,
    ):
        survey = Survey.objects.get(event__slug=input.event_slug, slug=input.survey_slug)

        graphql_check_instance(
            survey,
            info,
            app=survey.app,
            field="languages",
            operation="update",
        )

        promote_field_to_dimension(survey, input.field_slug)  # type: ignore

        return PromoteFieldToDimension(survey=survey)  # type: ignore
