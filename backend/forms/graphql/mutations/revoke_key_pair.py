import graphene
from django.http import HttpRequest

from ...models.keypair import KeyPair


class RevokeKeyPair(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)

    id = graphene.NonNull(graphene.String)

    @staticmethod
    def mutate(root, info, id: str):
        request: HttpRequest = info.context

        user = request.user
        if not user.is_authenticated:
            raise Exception("Not authenticated")

        keypair = KeyPair.objects.get(user=user, id=id)
        keypair.delete()

        return RevokeKeyPair(id=str(keypair.id))  # type: ignore
