import graphene
from graphene_django import DjangoObjectType

from kompassi.access.models.cbac_entry import CBACEntry
from kompassi.core.graphql.profile_limited import LimitedProfileType
from kompassi.core.models.person import Person


class SurveyAccessGrantType(DjangoObjectType):
    class Meta:
        model = CBACEntry
        fields = ("valid_until", "created_at")

    @staticmethod
    def resolve_person(entry: CBACEntry, info):
        return entry.user.person

    person = graphene.NonNull(LimitedProfileType)


class GrantablePersonType(DjangoObjectType):
    """
    A deliberately narrower profile than LimitedProfileType: grantablePeople is reachable
    by anyone with per-survey (not just event/organization-wide) access, so it must not
    expose contact details (email, phone, Discord handle) of everyone involved in the event.
    """

    class Meta:
        model = Person
        fields = ("id", "nick")

    @staticmethod
    def resolve_full_name(person: Person, info) -> str:
        return person.full_name

    full_name = graphene.NonNull(graphene.String)
