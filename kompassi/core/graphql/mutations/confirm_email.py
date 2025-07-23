import graphene
from django.contrib.auth.models import User
from django.http import HttpRequest

from ...models.person import Person
from ..user_limited import LimitedUserType


class ConfirmEmailInput(graphene.InputObjectType):
    locale = graphene.String(required=True)


class ConfirmEmail(graphene.Mutation):
    class Arguments:
        input = ConfirmEmailInput(required=True)

    user = graphene.Field(LimitedUserType)

    @staticmethod
    def mutate(
        root,
        info,
        input: ConfirmEmailInput,
    ):
        request: HttpRequest = info.context
        if not request.user.is_authenticated:
            raise Exception("User is not authenticated")

        user: User = request.user  # type: ignore
        person: Person = user.person  # type: ignore
        if not person:
            raise Exception("User is not a person")

        person.setup_email_verification(
            request,
            language=input.locale,  # type: ignore
        )

        return ConfirmEmail(user=user)  # type: ignore
