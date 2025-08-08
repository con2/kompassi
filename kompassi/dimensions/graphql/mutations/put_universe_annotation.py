from enum import Enum

import graphene
import pydantic
from django.db import transaction
from django.http import HttpRequest

from kompassi.access.cbac import graphql_check_instance

from ...models.annotation import Annotation
from ...models.scope import Scope
from ...models.universe_annotation import UniverseAnnotation
from ...tasks import universe_annotation_refresh_values
from ..universe_annotation_limited import LimitedUniverseAnnotationType

# too strict, users will be confounded
# ListOfSlugsAdapter = pydantic.TypeAdapter(list[Slug])
ListOfSlugsAdapter = pydantic.TypeAdapter(list[str])


class PutUniverseAnnotationAction(Enum):
    SAVE_WITHOUT_REFRESH = "SAVE_WITHOUT_REFRESH"
    SAVE_AND_REFRESH = "SAVE_AND_REFRESH"


PutUniverseAnnotationActionType = graphene.Enum.from_enum(PutUniverseAnnotationAction)


class PutUniverseAnnotationInput(graphene.InputObjectType):
    scope_slug = graphene.String(required=True)
    universe_slug = graphene.String(required=True)
    annotation_slug = graphene.String(required=True)
    is_active = graphene.Boolean(required=True)
    form_fields = graphene.InputField(
        graphene.List(graphene.NonNull(graphene.String)),
        required=True,
    )
    action = graphene.InputField(PutUniverseAnnotationActionType)


class PutUniverseAnnotation(graphene.Mutation):
    class Arguments:
        input = PutUniverseAnnotationInput(required=True)

    universe_annotation = graphene.Field(LimitedUniverseAnnotationType)

    @staticmethod
    def mutate(
        _root,
        info,
        input: PutUniverseAnnotationInput,
    ):
        request: HttpRequest = info.context
        scope = Scope.objects.get(slug=input.scope_slug)
        universe = scope.universes.get(slug=input.universe_slug)

        graphql_check_instance(
            universe,  # type: ignore
            request,
            app=universe.app,
            field="annotations",
            operation="update",
        )

        annotation = Annotation.objects.get(slug=input.annotation_slug)

        if annotation.is_internal and not input.is_active:
            raise ValueError("Internal annotations cannot be deactivated.")

        form_fields = ListOfSlugsAdapter.validate_python(input.form_fields)

        if input.action:
            action = PutUniverseAnnotationAction(input.action)
        else:
            action = PutUniverseAnnotationAction.SAVE_WITHOUT_REFRESH

        with transaction.atomic():
            universe_annotation, _ = UniverseAnnotation.objects.select_for_update(
                of=("self",),
                no_key=True,
            ).update_or_create(
                universe=universe,
                annotation=annotation,
                defaults=dict(
                    is_active=input.is_active,
                    form_fields=form_fields,
                ),
            )

        match action:
            case PutUniverseAnnotationAction.SAVE_WITHOUT_REFRESH:
                pass
            case PutUniverseAnnotationAction.SAVE_AND_REFRESH:
                if universe_annotation.is_active:
                    universe_annotation_refresh_values.delay(universe.id, annotation.id)  # type: ignore
            case _:
                raise NotImplementedError(action)

        return PutUniverseAnnotation(event_annotation=universe_annotation)  # type: ignore
