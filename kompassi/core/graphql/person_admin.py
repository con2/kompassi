from __future__ import annotations

import graphene

from ..models.person import Person
from .profile_limited import LimitedProfileType


class AdminPersonType(LimitedProfileType):
    """
    A person as seen by the site-wide user admin. Only reachable through the
    admin namespace, which checks the admin CBAC claims before returning any instance.
    """

    class Meta:
        model = Person
        fields = ("id", "first_name", "nick", "email", "discord_handle", "notes", "email_verified_at")

    @staticmethod
    def resolve_username(person: Person, info) -> str | None:
        return person.username

    username = graphene.String()

    @staticmethod
    def resolve_is_superuser(person: Person, info) -> bool:
        return bool(person.user and person.user.is_superuser)

    is_superuser = graphene.NonNull(graphene.Boolean)

    @staticmethod
    def resolve_is_active(person: Person, info) -> bool:
        return bool(person.user and person.user.is_active)

    is_active = graphene.NonNull(graphene.Boolean)

    @staticmethod
    def resolve_date_joined(person: Person, info):
        return person.user.date_joined if person.user else None

    date_joined = graphene.DateTime()

    @staticmethod
    def resolve_last_login(person: Person, info):
        return person.user.last_login if person.user else None

    last_login = graphene.DateTime()

    @staticmethod
    def resolve_groups(person: Person, info) -> list[str]:
        if person.user is None:
            return []
        return list(person.user.groups.order_by("name").values_list("name", flat=True))

    groups = graphene.NonNull(graphene.List(graphene.NonNull(graphene.String)))
