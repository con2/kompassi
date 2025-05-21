from typing import Any

import graphene
from django.db import transaction
from graphene.types.generic import GenericScalar

from access.cbac import graphql_check_instance
from program_v2.models.annotations import validate_annotations

from ...models.program import Program
from ..program_full import FullProgramType


class UpdateProgramAnnotationsInput(graphene.InputObjectType):
    event_slug = graphene.String(required=True)
    program_slug = graphene.String(required=True)
    annotations = GenericScalar(required=True)


class UpdateProgramAnnotations(graphene.Mutation):
    class Arguments:
        input = UpdateProgramAnnotationsInput(required=True)

    program = graphene.Field(FullProgramType)

    @transaction.atomic
    @staticmethod
    def mutate(
        _root,
        info,
        input: UpdateProgramAnnotationsInput,
    ):
        annotations: dict[str, Any] = input.annotations  # type: ignore
        validate_annotations(annotations)

        program = Program.objects.get(event__slug=input.event_slug, slug=input.program_slug)

        graphql_check_instance(
            program,
            info,
            field="annotations",
            operation="update",
        )

        program.annotations = dict(program.annotations, **input.annotations)  # type: ignore
        program.refresh_annotations()

        return UpdateProgramAnnotations(program=program)  # type: ignore
