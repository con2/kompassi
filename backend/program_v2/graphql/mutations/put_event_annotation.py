from enum import Enum

import graphene
import pydantic
from django.db import transaction
from django.http import HttpRequest

from access.cbac import graphql_check_instance
from core.models.event import Event
from dimensions.models.cached_dimensions import Slug

from ...models.annotation import Annotation
from ..annotation import EventAnnotationType

ListOfSlugsAdapter = pydantic.TypeAdapter(list[Slug])


class PutEventAnnotationAction(Enum):
    SAVE_WITHOUT_REFRESH = "SAVE_WITHOUT_REFRESH"
    SAVE_AND_REFRESH = "SAVE_AND_REFRESH"


PutEventAnnotationActionType = graphene.Enum.from_enum(PutEventAnnotationAction)


class PutEventAnnotationInput(graphene.InputObjectType):
    event_slug = graphene.String(required=True)
    annotation_slug = graphene.String(required=True)
    is_active = graphene.Boolean(required=True)
    program_form_fields = graphene.InputField(
        graphene.List(graphene.NonNull(graphene.String)),
        required=True,
    )
    action = graphene.InputField(PutEventAnnotationActionType)


class PutEventAnnotation(graphene.Mutation):
    class Arguments:
        input = PutEventAnnotationInput(required=True)

    event_annotation = graphene.Field(EventAnnotationType)

    @transaction.atomic
    @staticmethod
    def mutate(
        _root,
        info,
        input: PutEventAnnotationInput,
    ):
        request: HttpRequest = info.context
        event = Event.objects.get(slug=input.event_slug)
        graphql_check_instance(
            event,  # type: ignore
            request,
            app="program_v2",
            field="annotations",
            operation="update",
        )

        meta = event.program_v2_event_meta
        if meta is None:
            raise ValueError("Event does not have program_v2_event_meta.")

        annotation = Annotation.objects.get(slug=input.annotation_slug)

        if annotation.is_internal and not input.is_active:
            raise ValueError("Internal annotations cannot be deactivated.")

        program_form_fields = ListOfSlugsAdapter.validate_python(input.program_form_fields)

        if input.action:
            action = PutEventAnnotationAction(input.action)
        else:
            action = PutEventAnnotationAction.SAVE_WITHOUT_REFRESH

        event_annotation, _ = meta.event_annotations.update_or_create(
            annotation=annotation,
            defaults=dict(
                is_active=input.is_active,
                program_form_fields=program_form_fields,
                action=action,
            ),
        )

        return PutEventAnnotation(event_annotation=event_annotation)  # type: ignore
