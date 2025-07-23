from typing import Self

import graphene
from django import forms as django_forms

from kompassi.access.cbac import graphql_check_instance
from kompassi.core.utils.form_utils import camel_case_keys_to_snake_case
from kompassi.dimensions.models.enums import DimensionApp
from kompassi.forms.graphql.mutations.update_survey import UpdateSurveyInput
from kompassi.forms.graphql.survey_full import FullSurveyType
from kompassi.forms.models.survey import Survey


class ProgramFormForm(django_forms.ModelForm):
    class Meta:
        model = Survey
        fields = (
            "active_from",
            "active_until",
        )

    @classmethod
    def from_form_data(cls, survey: Survey, form_data: dict[str, str]) -> Self:
        form_data = camel_case_keys_to_snake_case(form_data)
        return cls(form_data, instance=survey)


class UpdateProgramForm(graphene.Mutation):
    class Arguments:
        input = UpdateSurveyInput(required=True)

    survey = graphene.Field(FullSurveyType)

    @staticmethod
    def mutate(
        root,
        info,
        input: UpdateSurveyInput,
    ):
        survey = Survey.objects.get(
            event__slug=input.event_slug,
            slug=input.survey_slug,
            app_name=DimensionApp.PROGRAM_V2.value,
        )
        form_data: dict[str, str] = input.form_data  # type: ignore

        graphql_check_instance(
            survey,
            info,
            app="program_v2",
            operation="update",
        )

        form = ProgramFormForm.from_form_data(survey, form_data)
        if not form.is_valid():
            raise django_forms.ValidationError(form.errors)  # type: ignore

        survey: Survey = form.save(commit=False)
        survey.with_mandatory_fields().save()

        survey.workflow.handle_form_update()
        return UpdateProgramForm(survey=survey)  # type: ignore
