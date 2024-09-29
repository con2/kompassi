from typing import Self

import graphene
from django import forms as django_forms
from graphene.types.generic import GenericScalar

from access.cbac import graphql_check_instance
from core.utils.form_utils import camel_case_keys_to_snake_case

from ...models.survey import Survey
from ..survey import SurveyType


class SurveyForm(django_forms.ModelForm):
    class Meta:
        model = Survey
        fields = ("login_required", "max_responses_per_user", "active_from", "active_until")

    @classmethod
    def from_form_data(cls, survey: Survey, form_data: dict[str, str]) -> Self:
        form_data = camel_case_keys_to_snake_case(form_data)
        return cls(form_data, instance=survey)


class UpdateSurveyInput(graphene.InputObjectType):
    event_slug = graphene.String(required=True)
    survey_slug = graphene.String(required=True)
    form_data = GenericScalar(required=True)


class UpdateSurvey(graphene.Mutation):
    class Arguments:
        input = UpdateSurveyInput(required=True)

    survey = graphene.Field(SurveyType)

    @staticmethod
    def mutate(
        root,
        info,
        input: UpdateSurveyInput,
    ):
        survey = Survey.objects.get(event__slug=input.event_slug, slug=input.survey_slug)
        form_data: dict[str, str] = input.form_data  # type: ignore

        # TODO(#324) rethink
        graphql_check_instance(survey, info, "self", "mutation")

        form = SurveyForm.from_form_data(survey, form_data)
        if not form.is_valid():
            raise django_forms.ValidationError(form.errors)  # type: ignore

        form.save()

        return UpdateSurvey(survey=survey)  # type: ignore
