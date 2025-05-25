from typing import Self

import graphene
from django import forms as django_forms

from access.cbac import graphql_check_instance
from core.utils.form_utils import camel_case_keys_to_snake_case
from forms.graphql.mutations.update_survey import UpdateSurveyInput
from forms.graphql.survey_full import FullSurveyType
from forms.models.survey import Survey, SurveyApp


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
            app="program_v2",
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
        survey = survey.with_mandatory_attributes_for_app(
            SurveyApp.PROGRAM_V2,
            purpose=survey.purpose,
        )
        survey.save()

        survey.workflow.handle_form_update()
        return UpdateProgramForm(survey=survey)  # type: ignore
