import graphene
from django.db import transaction
from django.http import HttpRequest

from kompassi.event_log_v2.utils.emit import emit

from ...models.survey import Survey


class DeleteSurveyResponsesInput(graphene.InputObjectType):
    event_slug = graphene.String(required=True)
    survey_slug = graphene.String(required=True)
    response_ids = graphene.List(graphene.String)


class DeleteSurveyResponses(graphene.Mutation):
    class Arguments:
        input = DeleteSurveyResponsesInput(required=True)

    count_deleted = graphene.NonNull(graphene.Int)

    @transaction.atomic
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

        _, deleted_by_model = survey.current_responses.filter(id__in=input.response_ids).delete()
        count_deleted = deleted_by_model.get("forms.Response", 0)

        _, deleted_by_model = survey.current_responses.filter(superseded_by__in=input.response_ids).delete()
        count_deleted += deleted_by_model.get("forms.Response", 0)

        emit(
            "forms.response.deleted",
            request=request,
            survey=survey.slug,
            organization=survey.event.organization.slug,
            event=survey.event.slug,
            count_deleted=count_deleted,
        )

        return DeleteSurveyResponses(count_deleted=count_deleted)  # type: ignore
