import graphene
from django.conf import settings
from django.http import HttpRequest
from graphene.types.generic import GenericScalar
from graphene_django import DjangoObjectType

from core.graphql.limited_event import LimitedEventType
from core.utils.text_utils import normalize_whitespace

from ..models.form import Form

DEFAULT_LANGUAGE: str = settings.LANGUAGE_CODE


class FormType(DjangoObjectType):
    class Meta:
        model = Form
        fields = (
            "title",
            "description",
            "thank_you_message",
            "language",
            "survey",
        )

    @staticmethod
    def resolve_fields(parent: Form, info, enrich: bool = True):
        if enrich:
            return parent.cached_enriched_fields
        else:
            return parent.fields

    fields = graphene.Field(
        GenericScalar,
        enrich=graphene.Boolean(
            description=(
                "Enriched fields have dynamic choices populated for them. This is the default. "
                'Pass enrich: false to get access to "raw" unenriched fields. This is used by the form editor.'
            ),
        ),
    )

    @staticmethod
    def resolve_event(parent: Form, info):
        return parent.event

    event = graphene.Field(graphene.NonNull(LimitedEventType))

    @staticmethod
    def resolve_can_remove(form: Form, info):
        """
        A form can be removed if it has no responses.
        """
        request: HttpRequest = info.context
        return form.can_be_deleted_by(request)

    can_remove = graphene.NonNull(
        graphene.Boolean,
        description=normalize_whitespace(resolve_can_remove.__doc__ or ""),
    )
