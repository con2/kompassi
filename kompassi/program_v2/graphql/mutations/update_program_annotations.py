import graphene
from django.db import transaction
from django.http import HttpRequest
from graphene.types.generic import GenericScalar

from kompassi.access.cbac import graphql_check_instance
from kompassi.core.models.event import Event
from kompassi.dimensions.models.cached_annotations import cached_annotations_update_adapter, validate_annotations
from kompassi.dimensions.models.enums import AnnotationAppliesTo, AnnotationDataType, AnnotationFlags

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

        program = Program.objects.get(event__slug=input.event_slug, slug=input.program_slug)

        graphql_check_instance(
            program,
            request,
            field="annotations",
            operation="update",
        )

        # values "" and None used to indicate "remove this annotation"
        input_annotations = cached_annotations_update_adapter.validate_python(input.annotations)

        # validate only the annotations we are setting (do not contain "" or None)
        set_annotations = {k: v for (k, v) in input_annotations.items() if v not in (None, "")}
        schema = (
            meta.annotations_with_fallback.filter(
                applies_to__has_all=AnnotationAppliesTo.PROGRAM_ITEM,
            )
            .exclude(
                # Value of computed annotations cannot be set directly
                flags__has_all=AnnotationFlags.COMPUTED,
            )
            .exclude(
                # TODO(#951) Timezone handling for DATETIME annotations is broken
                type=AnnotationDataType.DATETIME,
            )
        )
        validate_annotations(set_annotations, schema)

        # yes, use input_annotations here instead of set_annotations,
        # because we want to remove annotations with empty values
        program.refresh_annotations(input_annotations)
        program.refresh_dependents()

        return UpdateProgramAnnotations(program=program)  # type: ignore
