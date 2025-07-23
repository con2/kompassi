from typing import Self

import graphene
from django import forms as django_forms
from graphene.types.generic import GenericScalar

from kompassi.access.cbac import graphql_check_instance
from kompassi.core.utils.form_utils import camel_case_keys_to_snake_case
from kompassi.program_v2.graphql.program_full import FullProgramType
from kompassi.program_v2.models.program import Program


class ProgramForm(django_forms.ModelForm):
    class Meta:
        model = Program
        fields = (
            "title",
            "description",
        )

    @classmethod
    def from_form_data(cls, program: Program, form_data: dict[str, str]) -> Self:
        form_data = camel_case_keys_to_snake_case(form_data)
        return cls(form_data, instance=program)


class UpdateProgramInput(graphene.InputObjectType):
    event_slug = graphene.String(required=True)
    program_slug = graphene.String(required=True)
    form_data = GenericScalar(required=True)


class UpdateProgram(graphene.Mutation):
    class Arguments:
        input = UpdateProgramInput(required=True)

    program = graphene.Field(FullProgramType)

    @staticmethod
    def mutate(
        root,
        info,
        input: UpdateProgramInput,
    ):
        program = Program.objects.get(
            event__slug=input.event_slug,
            slug=input.program_slug,
        )
        form_data: dict[str, str] = input.form_data  # type: ignore

        graphql_check_instance(
            program,
            info,
            operation="update",
        )

        form = ProgramForm.from_form_data(program, form_data)
        if not form.is_valid():
            raise django_forms.ValidationError(form.errors)  # type: ignore

        program: Program = form.save()

        return UpdateProgram(program=program)  # type: ignore
