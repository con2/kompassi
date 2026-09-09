from __future__ import annotations

import graphene
from graphene.types.generic import GenericScalar
from graphene_django import DjangoObjectType

from kompassi.core.graphql.profile_limited import LimitedProfileType
from kompassi.core.models.person import Person

from ..models.entry import Entry


class LimitedEventLogEntryType(DjangoObjectType):
    class Meta:
        model = Entry
        fields = ("id", "entry_type")

    @staticmethod
    def resolve_created_at(entry: Entry, info):
        return entry.created_at

    created_at = graphene.NonNull(graphene.DateTime)

    @staticmethod
    def resolve_actor(entry: Entry, info) -> Person | None:
        # entry.actor.person is Django's reverse OneToOne accessor: it raises DoesNotExist,
        # rather than returning None, when the actor has no Person.
        if entry.actor_id is None:
            return None
        try:
            return entry.actor.person
        except Person.DoesNotExist:
            return None

    actor = graphene.Field(LimitedProfileType)

    @staticmethod
    def resolve_message(entry: Entry, info) -> str:
        return entry.message

    message = graphene.NonNull(graphene.String)

    @staticmethod
    def resolve_other_fields(entry: Entry, info) -> dict:
        return entry.other_fields

    other_fields = graphene.NonNull(GenericScalar)
