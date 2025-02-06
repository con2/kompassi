import graphene
from django.http import HttpRequest

from dimensions.models.dimension_value import DimensionValue

from ...models.survey import Survey


class DeleteSurveyDimensionValueInput(graphene.InputObjectType):
    event_slug = graphene.String(required=True)
    survey_slug = graphene.String(required=True)
    dimension_slug = graphene.String(required=True)
    value_slug = graphene.String(required=True)


class DeleteSurveyDimensionValue(graphene.Mutation):
    class Arguments:
        input = DeleteSurveyDimensionValueInput(required=True)

    slug = graphene.Field(graphene.String)

    @staticmethod
    def mutate(
        root,
        info,
        input: DeleteSurveyDimensionValueInput,
    ):
        request: HttpRequest = info.context
        survey = Survey.objects.get(event__slug=input.event_slug, slug=input.survey_slug)
        value = DimensionValue.objects.get(
            dimension__universe=survey.universe,
            dimension__slug=input.dimension_slug,
            slug=input.value_slug,
        )
        if not value.can_be_deleted_by(request):
            raise Exception("Cannot remove dimension value")

        value.delete()

        return DeleteSurveyDimensionValue(slug=input.survey_slug)  # type: ignore
