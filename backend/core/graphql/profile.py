import graphene
from graphene_django import DjangoObjectType

from core.models import Person
from core.utils import normalize_whitespace
from forms.graphql.meta import FormsProfileMetaType
from forms.models.meta import FormsProfileMeta
from program_v2.graphql.meta import ProgramV2ProfileMetaType
from program_v2.models.meta import ProgramV2ProfileMeta


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

    @staticmethod
    def resolve_program(person: Person, info):
        """
        Namespace for queries related to programs and the current user.
        """
        return ProgramV2ProfileMeta(person)

    program = graphene.Field(
        graphene.NonNull(ProgramV2ProfileMetaType),
        description=normalize_whitespace(resolve_program.__doc__ or ""),
    )
