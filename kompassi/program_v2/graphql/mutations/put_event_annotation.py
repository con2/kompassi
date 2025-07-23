from enum import Enum

import graphene
import pydantic
from django.db import transaction
from django.http import HttpRequest

from kompassi.access.cbac import graphql_check_instance
from kompassi.core.models.event import Event
from kompassi.program_v2.models.event_annotation import EventAnnotation
from kompassi.program_v2.tasks import event_annotation_refresh_values

from ...models.annotation import Annotation
from ..annotation import EventAnnotationType

# too strict, users will be confounded
# ListOfSlugsAdapter = pydantic.TypeAdapter(list[Slug])
ListOfSlugsAdapter = pydantic.TypeAdapter(list[str])


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

        with transaction.atomic():
            event_annotation, _ = EventAnnotation.objects.select_for_update(
                of=("self",),
                no_key=True,
            ).update_or_create(
                meta=meta,
                annotation=annotation,
                defaults=dict(
                    is_active=input.is_active,
                    program_form_fields=program_form_fields,
                    action=action,
                ),
            )

        match action:
            case PutEventAnnotationAction.SAVE_WITHOUT_REFRESH:
                pass
            case PutEventAnnotationAction.SAVE_AND_REFRESH:
                if event_annotation.is_active:
                    event_annotation_refresh_values.delay(event.id, annotation.id)  # type: ignore
            case _:
                raise NotImplementedError(action)

        return PutEventAnnotation(event_annotation=event_annotation)  # type: ignore
