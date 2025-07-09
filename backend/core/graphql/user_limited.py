import graphene
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from graphene_django import DjangoObjectType

from core.models.person import Person


class LimitedUserType(DjangoObjectType):
    """
    Deprecated. Use ProfileType instead.
    """

    @staticmethod
    def resolve_display_name(user: AbstractUser, info):
        person: Person | None = user.person  # type: ignore
        return person.full_name if person else user.get_full_name()

    display_name = graphene.Field(
        graphene.NonNull(graphene.String),
        description="User's full name.",
    )

    class Meta:
        model = get_user_model()
        fields = ("email", "first_name", "last_name")
