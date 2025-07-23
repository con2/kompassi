import graphene
from graphene_django import DjangoObjectType

from ..models.keypair import KeyPair


class KeyPairType(DjangoObjectType):
    @staticmethod
    def resolve_created_at(keypair: KeyPair, info):
        return keypair.timestamp

    created_at = graphene.NonNull(graphene.DateTime)

    class Meta:
        model = KeyPair
        fields = (
            "id",
            "public_key",
        )
