import graphene
from django.db import transaction
from django.http import HttpRequest

from ...models.survey import Survey


class DeleteSurveyInput(graphene.InputObjectType):
    event_slug = graphene.String(required=True)
    survey_slug = graphene.String(required=True)


class DeleteSurvey(graphene.Mutation):
    class Arguments:
        input = DeleteSurveyInput(required=True)

    slug = graphene.Field(graphene.String)

    @staticmethod
    def mutate(
        root,
        info,
        input: DeleteSurveyInput,
    ):
        survey = Survey.objects.get(
            event__slug=input.event_slug,
            slug=input.survey_slug,
        )

        request: HttpRequest = info.context
        if not survey.can_be_deleted_by(request):
            raise Exception("Cannot delete survey")

        with transaction.atomic():
            survey.workflow.revoke_all_access(request)
            # language versions (Forms) are deleted by cascade
            survey.delete()

        return DeleteSurvey(slug=input.survey_slug)  # type: ignore
