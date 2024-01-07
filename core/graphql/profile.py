import graphene
from graphene_django import DjangoObjectType

from core.models import Person
from core.utils import normalize_whitespace
from forms.graphql.meta import FormsProfileMetaType
from forms.models.meta import FormsProfileMeta


class ProfileType(DjangoObjectType):
    class Meta:
        model = Person
        fields = ("first_name", "nick", "email")

    @staticmethod
    def resolve_last_name(person: Person, info):
        return person.surname

    last_name = graphene.Field(graphene.String)

    @staticmethod
    def resolve_phone_number(person: Person, info):
        return person.normalized_phone_number

    phone_number = graphene.Field(graphene.String)

    @staticmethod
    def resolve_display_name(person: Person, info):
        return person.display_name

    display_name = graphene.Field(graphene.String)

    @staticmethod
    def resolve_forms(person: Person, info):
        """
        Namespace for queries related to forms and the current user.
        """
        return FormsProfileMeta(person)

    forms = graphene.Field(
        graphene.NonNull(FormsProfileMetaType),
        description=normalize_whitespace(resolve_forms.__doc__ or ""),
    )
