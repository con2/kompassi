import graphene
from graphene_django import DjangoObjectType

from forms.graphql.form import FormType
from forms.models import Form
from graphql_api.utils import DEFAULT_LANGUAGE, resolve_localized_field

from ..models import (
    OfferForm,
)


class OfferFormType(DjangoObjectType):
    form = graphene.Field(FormType, lang=graphene.String())

    @staticmethod
    def resolve_form(
        parent: OfferForm,
        info,
        lang: str = DEFAULT_LANGUAGE,
    ) -> Form | None:
        return parent.get_form(lang)

    is_active = graphene.Field(graphene.NonNull(graphene.Boolean))

    @staticmethod
    def resolve_is_active(parent: OfferForm, info) -> bool:
        return parent.is_active

    short_description = graphene.String(lang=graphene.String())
    resolve_short_description = resolve_localized_field("short_description")

    class Meta:
        model = OfferForm
        fields = ("slug",)
