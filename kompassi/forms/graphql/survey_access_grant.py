import graphene
from graphene_django import DjangoObjectType

from kompassi.access.models.cbac_entry import CBACEntry
from kompassi.core.graphql.profile_limited import LimitedProfileType


class SurveyAccessGrantType(DjangoObjectType):
    class Meta:
        model = CBACEntry
        fields = ("valid_until", "created_at")

    @staticmethod
    def resolve_person(entry: CBACEntry, info):
        return entry.user.person

    person = graphene.NonNull(LimitedProfileType)
