import graphene
import graphene_django

from involvement.models.involvement import Involvement


class LimitedInvolvementType(graphene_django.DjangoObjectType):
    """
    Represent Involvement (and the Person involved) without a way to traverse back to Event.
    """

    class Meta:
        model = Involvement
        fields = ("id", "is_active", "created_at", "updated_at")
        description = "Limited program host type. Used for the program host field in the program list."

    # TODO a cleaner way to delegate to Person?

    @staticmethod
    def resolve_first_name(involvement: Involvement, info) -> str:
        return involvement.person.first_name

    first_name = graphene.NonNull(graphene.String)

    @staticmethod
    def resolve_last_name(involvement: Involvement, info) -> str:
        return involvement.person.surname

    last_name = graphene.NonNull(graphene.String)

    @staticmethod
    def resolve_email(involvement: Involvement, info) -> str:
        return involvement.person.email

    email = graphene.NonNull(graphene.String)

    @staticmethod
    def resolve_phone_number(involvement: Involvement, info) -> str:
        return involvement.person.normalized_phone_number

    phone_number = graphene.NonNull(graphene.String)

    @staticmethod
    def resolve_nick(involvement: Involvement, info) -> str:
        return involvement.person.nick

    nick = graphene.NonNull(graphene.String)
