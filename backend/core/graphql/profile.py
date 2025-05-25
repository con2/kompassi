import graphene
from graphene_django import DjangoObjectType

from core.models import Person
from core.utils import normalize_whitespace
from forms.graphql.keypair import KeyPairType
from forms.graphql.meta import FormsProfileMetaType
from forms.models.keypair import KeyPair
from forms.models.meta import FormsProfileMeta
from program_v2.graphql.meta import ProgramV2ProfileMetaType
from program_v2.models.meta import ProgramV2ProfileMeta
from tickets_v2.graphql.meta import TicketsV2ProfileMetaType
from tickets_v2.models.meta import TicketsV2ProfileMeta


class ProfileType(DjangoObjectType):
    class Meta:
        model = Person
        fields = ("first_name", "nick", "email", "discord_handle")

    @staticmethod
    def resolve_last_name(person: Person, info):
        return person.surname

    last_name = graphene.NonNull(graphene.String)

    @staticmethod
    def resolve_phone_number(person: Person, info):
        return person.normalized_phone_number

    phone_number = graphene.NonNull(graphene.String)

    @staticmethod
    def resolve_display_name(person: Person, info):
        return person.display_name

    display_name = graphene.NonNull(graphene.String)

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

    @staticmethod
    def resolve_tickets(person: Person, info):
        """
        Namespace for queries related to tickets and the current user.
        """
        return TicketsV2ProfileMeta(person)

    tickets = graphene.Field(
        graphene.NonNull(TicketsV2ProfileMetaType),
        description=normalize_whitespace(resolve_tickets.__doc__ or ""),
    )

    @staticmethod
    def resolve_keypairs(person: Person, info):
        return person.user.keypairs.all() if person.user else KeyPair.objects.none()

    keypairs = graphene.List(
        graphene.NonNull(KeyPairType),
        description=normalize_whitespace(resolve_keypairs.__doc__ or ""),
    )
