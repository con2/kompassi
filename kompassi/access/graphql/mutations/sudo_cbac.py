import graphene
from django.http import HttpRequest
from graphene.types.generic import GenericScalar

from ...sudo import grant_sudo


class SudoCbacInput(graphene.InputObjectType):
    claims = GenericScalar(required=True)


class SudoCbac(graphene.Mutation):
    """
    Lets a superuser override a CBAC denial by minting a temporary CBAC entry for the
    given claims. Mirrors V1's sudo_view (kompassi/access/views/sudo_view.py); both call
    grant_sudo, which re-checks is_superuser and re-filters claims to CBAC_SUDO_CLAIMS,
    so a tampered request cannot escalate past what a superuser could already grant itself.
    """

    class Arguments:
        input = SudoCbacInput(required=True)

    valid_until = graphene.DateTime()

    @staticmethod
    def mutate(
        root,
        info,
        input: SudoCbacInput,
    ):
        request: HttpRequest = info.context
        claims: dict[str, str] = input.claims  # type: ignore

        cbac_entry = grant_sudo(request.user, claims, request=request)

        return SudoCbac(valid_until=cbac_entry.valid_until)  # type: ignore
