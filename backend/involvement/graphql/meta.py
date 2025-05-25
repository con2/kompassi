from __future__ import annotations

import graphene
from django.http import HttpRequest

from ..models.meta import InvolvementEventMeta
from .invitation_full import FullInvitationType


class InvolvementEventMetaType(graphene.ObjectType):
    @staticmethod
    def resolve_invitation(
        meta: InvolvementEventMeta,
        info,
        invitation_id: str,
    ):
        request: HttpRequest = info.context

        if not request.user.is_authenticated:
            raise Exception("User is not authenticated")

        return meta.invitations.get(id=invitation_id)

    invitation = graphene.Field(
        FullInvitationType,
        invitation_id=graphene.String(required=True),
    )
