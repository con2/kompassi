import graphene

from kompassi.core.models import Person
from kompassi.core.utils import normalize_whitespace
from kompassi.forms.graphql.keypair import KeyPairType
from kompassi.forms.graphql.meta import FormsProfileMetaType
from kompassi.forms.models.keypair import KeyPair
from kompassi.forms.models.meta import FormsProfileMeta
from kompassi.program_v2.graphql.meta import ProgramV2ProfileMetaType
from kompassi.program_v2.models.meta import ProgramV2ProfileMeta
from kompassi.tickets_v2.graphql.meta import TicketsV2ProfileMetaType
from kompassi.tickets_v2.models.meta import TicketsV2ProfileMeta

from .profile_limited import LimitedProfileType


class OwnProfileType(LimitedProfileType):
    class Meta:
        model = Person
        fields = ("id", "first_name", "nick", "email", "discord_handle")

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
