import graphene
from graphene.types.generic import GenericScalar
from graphene_django import DjangoObjectType

from ..models import (
    Program,
)

# imported for side effects (register object type used by django object type fields)
from .schedule import ScheduleItemType  # noqa: F401


class ProgramType(DjangoObjectType):
    cached_dimensions = graphene.Field(GenericScalar)

    @staticmethod
    def resolve_cached_hosts(parent: Program, info):
        return parent.other_fields.get("formatted_hosts", "")

    cached_hosts = graphene.NonNull(graphene.String)

    @staticmethod
    def resolve_signup_link(parent: Program, info):
        return parent.other_fields.get("signup_link", "")

    signup_link = graphene.NonNull(graphene.String)

    class Meta:
        model = Program
        fields = ("title", "slug", "description", "dimensions", "cached_dimensions", "schedule_items")
