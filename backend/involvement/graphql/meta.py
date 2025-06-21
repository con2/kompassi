from __future__ import annotations

import graphene
from django.http import HttpRequest

from access.cbac import graphql_check_model
from dimensions.filters import DimensionFilters
from dimensions.graphql.dimension_filter_input import DimensionFilterInput

from ..models.involvement import Involvement
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

    @staticmethod
    def resolve_people(
        meta: InvolvementEventMeta,
        info,
        filters: list[DimensionFilterInput] | None = None,
    ):
        request: HttpRequest = info.context

        graphql_check_model(
            Involvement,
            meta.event.scope,
            request,
        )

        involvements = DimensionFilters.from_graphql(filters).filter(
            meta.event.involvements.all().select_related("person").order_by("person__surname", "person__first_name")
        )
