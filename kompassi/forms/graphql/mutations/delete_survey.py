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
        request: HttpRequest = info.context

        with transaction.atomic():
            survey = Survey.objects.select_for_update().get(
                event__slug=input.event_slug,
                slug=input.survey_slug,
            )
            # Lock the language versions so that no response can be created between the check and the delete
            list(survey.languages.select_for_update())

            if not survey.can_be_deleted_by(request):
                raise Exception("Cannot delete survey")

            survey.workflow.revoke_all_access(request)
            # language versions (Forms) and pending invitations are deleted by cascade
            survey.delete()

        return DeleteSurvey(slug=input.survey_slug)  # type: ignore
