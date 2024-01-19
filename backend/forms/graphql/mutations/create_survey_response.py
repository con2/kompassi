from typing import Any

import graphene
from graphene.types.generic import GenericScalar

from core.utils import get_ip

from ...models.response import Response
from ...models.survey import Survey
from ..response import FullResponseType


class CreateSurveyResponse(graphene.Mutation):
    class Arguments:
        event_slug = graphene.String(required=True)
        survey_slug = graphene.String(required=True)
        form_data = GenericScalar(required=True)
        locale = graphene.String()

    response = graphene.Field(FullResponseType)

    @staticmethod
    def mutate(
        root,
        info,
        event_slug: str,
        survey_slug: str,
        form_data: dict[str, Any],
        locale: str = "",
    ):
        survey = Survey.objects.get(event__slug=event_slug, slug=survey_slug)

        if not survey.is_active:
            raise Exception("Survey is not active")

        form = survey.get_form(locale)
        if not form:
            raise Exception("Form not found")

        if not form.fields:
            raise Exception("Form has no fields")

        # TODO(https://github.com/con2/kompassi/issues/365): shows the ip of v2 backend, not the client
        ip_address = get_ip(info.context)
        created_by = user if (user := info.context.user) and user.is_authenticated else None

        if survey.login_required and not created_by:
            raise Exception("Login required")

        if survey.max_responses_per_user:  # noqa: SIM102
            if survey.responses.filter(created_by=created_by).count() >= survey.max_responses_per_user:
                raise Exception("Maximum number of responses reached")

        if survey.anonymity == "hard":
            created_by = None
            ip_address = ""

        response = Response.objects.create(
            form=form,
            form_data=form_data,
            created_by=created_by,
            ip_address=ip_address,
        )

        response.lift_dimension_values()

        return CreateSurveyResponse(response=response)  # type: ignore
