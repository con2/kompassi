import graphene
from django.db import transaction
from django.http import HttpRequest
from graphene.types.generic import GenericScalar

from access.cbac import graphql_check_instance
from core.models.event import Event

from ...models.cached_annotations import compact_annotations, validate_annotations
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
        request: HttpRequest = info.context

        event = Event.objects.get(slug=input.event_slug)
        meta = event.program_v2_event_meta
        if meta is None:
            raise ValueError("Event does not have program metadata.")

        schema = meta.annotations_with_fallback.filter(is_computed=False)
        annotations = validate_annotations(input.annotations, schema)
        program = Program.objects.get(event__slug=input.event_slug, slug=input.program_slug)

        graphql_check_instance(
            program,
            request,
            field="annotations",
            operation="update",
        )

        program.annotations = compact_annotations(dict(program.annotations, **annotations))  # type: ignore
        program.refresh_annotations()

        return UpdateProgramAnnotations(program=program)  # type: ignore
