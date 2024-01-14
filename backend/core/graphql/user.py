import graphene
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from graphene_django import DjangoObjectType


# TODO should we use Person instead?
class LimitedUserType(DjangoObjectType):
    @staticmethod
    def resolve_display_name(user: AbstractUser, info):
        return user.get_full_name()

    display_name = graphene.Field(
        graphene.NonNull(graphene.String),
        description="User's full name.",
    )

    class Meta:
        model = get_user_model()
        fields = ("email", "first_name", "last_name")
