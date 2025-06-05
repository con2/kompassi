import graphene
from django.db import transaction
from django.http import HttpRequest
from graphene.types.generic import GenericScalar

from access.cbac import graphql_check_instance
from core.utils import get_ip

from ...models.enums import SurveyPurpose
from ...models.response import Response
from ...models.survey import Survey
from ..response_profile import ProfileResponseType


class CreateSurveyResponseInput(graphene.InputObjectType):
    locale = graphene.String()
    event_slug = graphene.String(required=True)
    survey_slug = graphene.String(required=True)
    edit_response_id = graphene.String()
    form_data = GenericScalar(required=True)


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
        request: HttpRequest = info.context
        survey = Survey.objects.get(event__slug=input.event_slug, slug=input.survey_slug)

        form = survey.get_form(input.locale)  # type: ignore
        if not form:
            raise Exception("Form not found")

        # TODO(https://github.com/con2/kompassi/issues/365): shows the ip of v2 backend, not the client
        ip_address = get_ip(info.context)
        revision_created_by = user if (user := info.context.user) and user.is_authenticated else None

        if input.edit_response_id:
            try:
                old_version = survey.all_responses.get(id=input.edit_response_id)
            except Response.DoesNotExist as e:
                raise Exception("Response to edit not found") from e

            if not survey.workflow.response_can_be_edited_by(old_version, request):
                raise Exception("Response cannot be edited by the user")

            original_created_by = old_version.original_created_by
            original_created_at = old_version.original_created_at
        else:
            old_version = None
            original_created_by = None
            original_created_at = None

            if not survey.is_active:
                graphql_check_instance(
                    survey,
                    request,
                    app=survey.app,
                    field="responses",
                    operation="create",
                )

            if survey.login_required and not revision_created_by:
                raise Exception("Login required")

            if survey.max_responses_per_user:  # noqa: SIM102
                if (
                    survey.current_responses.filter(revision_created_by=revision_created_by).count()
                    >= survey.max_responses_per_user
                ):
                    raise Exception("Maximum number of responses reached")

        if survey.purpose != SurveyPurpose.DEFAULT and old_version is None:
            raise Exception("Special purpose surveys cannot be submitted via this endpoint")

        if survey.anonymity == "HARD":
            revision_created_by = None
            ip_address = ""

        with transaction.atomic():
            response = Response.objects.create(
                form=form,
                form_data=input.form_data,
                revision_created_by=revision_created_by,
                ip_address=ip_address,
                sequence_number=survey.get_next_sequence_number(),
                original_created_by=original_created_by or revision_created_by,
                original_created_at=original_created_at,
            )

            if old_version:
                old_version.superseded_by = response
                old_version.save(update_fields=["superseded_by"])
                survey.all_responses.filter(superseded_by=old_version).update(superseded_by=response)

            survey.workflow.handle_new_response_phase1(response)

        survey.workflow.handle_new_response_phase2(response)
        return CreateSurveyResponse(response=response)  # type: ignore
