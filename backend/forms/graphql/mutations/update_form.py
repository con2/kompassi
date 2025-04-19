from typing import Self

import graphene
from django import forms as django_forms
from graphene.types.generic import GenericScalar

from access.cbac import graphql_check_instance
from core.utils.form_utils import camel_case_keys_to_snake_case

from ...models.form import Form
from ...models.survey import Survey
from ..survey_full import FullSurveyType


class FormForm(django_forms.ModelForm):
    """
    Yo dawg
    We heard you like forms
    So we made a form for your form
    """

    class Meta:
        model = Form
        fields = ("title", "description", "thank_you_message")

    @classmethod
    def from_form_data(cls, survey: Form, form_data: dict[str, str]) -> Self:
        form_data = camel_case_keys_to_snake_case(form_data)
        return cls(form_data, instance=survey)


class UpdateFormInput(graphene.InputObjectType):
    event_slug = graphene.String(required=True)
    survey_slug = graphene.String(required=True)
    language = graphene.String(required=True)
    form_data = GenericScalar(required=True)


class UpdateForm(graphene.Mutation):
    class Arguments:
        input = UpdateFormInput(required=True)

    survey = graphene.Field(FullSurveyType)

    @staticmethod
    def mutate(
        root,
        info,
        input: UpdateFormInput,
    ):
        survey = Survey.objects.get(event__slug=input.event_slug, slug=input.survey_slug)
        form = survey.languages.get(language=input.language)
        form_data: dict[str, str] = input.form_data  # type: ignore

        graphql_check_instance(
            survey,
            info,
            app=survey.app,
            field="languages",
            operation="update",
        )

        form_form = FormForm.from_form_data(form, form_data)
        if not form_form.is_valid():
            raise django_forms.ValidationError(form_form.errors)  # type: ignore

        form_form.save()

        survey.workflow.handle_form_update()
        return UpdateForm(survey=survey)  # type: ignore
