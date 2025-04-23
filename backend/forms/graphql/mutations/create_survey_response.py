import graphene
from django.db import transaction
from graphene.types.generic import GenericScalar

from access.cbac import graphql_check_instance
from core.utils import get_ip

from ...models.response import Response
from ...models.survey import Survey
from ..response_profile import ProfileResponseType


class CreateSurveyResponseInput(graphene.InputObjectType):
    event_slug = graphene.String(required=True)
    survey_slug = graphene.String(required=True)
    form_data = GenericScalar(required=True)
    locale = graphene.String()


class CreateSurveyResponse(graphene.Mutation):
    class Arguments:
        input = CreateSurveyResponseInput(required=True)

    response = graphene.Field(ProfileResponseType)

    @staticmethod
    def mutate(
        root,
        info,
        input: CreateSurveyResponseInput,
    ):
        survey = Survey.objects.get(event__slug=input.event_slug, slug=input.survey_slug)

        if not survey.is_active:
            graphql_check_instance(
                survey,
                info,
                app=survey.app,
                field="responses",
                operation="create",
            )

        form = survey.get_form(input.locale)  # type: ignore
        if not form:
            raise Exception("Form not found")

        # TODO(https://github.com/con2/kompassi/issues/365): shows the ip of v2 backend, not the client
        ip_address = get_ip(info.context)
        created_by = user if (user := info.context.user) and user.is_authenticated else None

        if survey.login_required and not created_by:
            raise Exception("Login required")

        if survey.max_responses_per_user:  # noqa: SIM102
            if survey.responses.filter(created_by=created_by).count() >= survey.max_responses_per_user:
                raise Exception("Maximum number of responses reached")

        if survey.anonymity == "HARD":
            created_by = None
            ip_address = ""

        with transaction.atomic():
            response = Response.objects.create(
                form=form,
                form_data=input.form_data,
                created_by=created_by,
                ip_address=ip_address,
                sequence_number=survey.get_next_sequence_number(),
            )

            response.lift_dimension_values()

        survey.workflow.handle_new_response(response)
        return CreateSurveyResponse(response=response)  # type: ignore
