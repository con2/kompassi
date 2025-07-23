import graphene
from django.http import HttpRequest

from ...models.keypair import KeyPair


class GenerateKeyPair(graphene.Mutation):
    class Arguments:
        password = graphene.String(required=True)

    id = graphene.NonNull(graphene.String)

    @staticmethod
    def mutate(root, info, password: str):
        request: HttpRequest = info.context

        user = request.user
        if not user.is_authenticated:
            raise Exception("Not authenticated")

        keypair = KeyPair.generate_for_user(user, password)  # type: ignore

        return GenerateKeyPair(id=str(keypair.id))  # type: ignore
