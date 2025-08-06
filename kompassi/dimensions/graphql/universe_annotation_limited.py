from graphene_django import DjangoObjectType

from ..models.universe_annotation import UniverseAnnotation


class LimitedUniverseAnnotationType(DjangoObjectType):
    class Meta:
        model = UniverseAnnotation
        fields = (
            "annotation",
            "is_active",
            "form_fields",
        )
