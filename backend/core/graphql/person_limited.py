from __future__ import annotations

import graphene
import graphene_django

from ..models.person import Person


class LimitedPersonType(graphene_django.DjangoObjectType):
    """
    Represent Person without a way to traverse back to Event.
    """

    class Meta:
        model = Person
        fields = ("id", "first_name", "nick", "email", "discord_handle")

    # The Queen is dead, long live the Queen!
    @staticmethod
    def resolve_last_name(person: Person, info) -> str:
        return person.surname

    last_name = graphene.NonNull(graphene.String)

    @staticmethod
    def resolve_phone_number(person: Person, info) -> str:
        return person.normalized_phone_number

    phone_number = graphene.NonNull(graphene.String)

    @staticmethod
    def resolve_full_name(person: Person, info) -> str:
        return person.full_name

    full_name = graphene.NonNull(graphene.String)
