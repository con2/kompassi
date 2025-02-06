import graphene
from django.http import HttpRequest

from ...models.survey import Survey


class DeleteSurveyDimensionInput(graphene.InputObjectType):
    event_slug = graphene.String(required=True)
    survey_slug = graphene.String(required=True)
    dimension_slug = graphene.String(required=True)


class DeleteSurveyDimension(graphene.Mutation):
    class Arguments:
        input = DeleteSurveyDimensionInput(required=True)

    slug = graphene.Field(graphene.String)

    @staticmethod
    def mutate(
        root,
        info,
        input: DeleteSurveyDimensionInput,
    ):
        request: HttpRequest = info.context
        survey = Survey.objects.get(event__slug=input.event_slug, slug=input.survey_slug)
        dimension = survey.dimensions.get(slug=input.dimension_slug)
        if not dimension.can_be_deleted_by(request):
            raise Exception("Cannot remove dimension")

        dimension.delete()

        return DeleteSurveyDimension(slug=input.survey_slug)  # type: ignore
