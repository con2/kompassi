import graphene
from django.http import HttpRequest

from ...models.survey import Survey


class DeleteSurveyResponsesInput(graphene.InputObjectType):
    event_slug = graphene.String(required=True)
    survey_slug = graphene.String(required=True)
    response_ids = graphene.List(graphene.String)


class DeleteSurveyResponses(graphene.Mutation):
    class Arguments:
        input = DeleteSurveyResponsesInput(required=True)

    count_deleted = graphene.NonNull(graphene.Int)

    @staticmethod
    def mutate(
        root,
        info,
        input: DeleteSurveyResponsesInput,
    ):
        survey = Survey.objects.get(event__slug=input.event_slug, slug=input.survey_slug)

        request: HttpRequest = info.context
        if not survey.can_responses_be_deleted_by(request):
            raise ValueError("Cannot delete responses")

        queryset = survey.current_responses.filter(id__in=input.response_ids)
        _, deleted_by_model = queryset.delete()
        count_deleted = deleted_by_model.get("forms.Response", 0)

        return DeleteSurveyResponses(count_deleted=count_deleted)  # type: ignore
