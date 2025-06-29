from __future__ import annotations

import graphene
from django.http import HttpRequest

from access.cbac import graphql_check_instance, graphql_check_model
from core.utils.text_utils import normalize_whitespace
from dimensions.filters import DimensionFilters
from dimensions.graphql.dimension_filter_input import DimensionFilterInput
from dimensions.graphql.dimension_full import FullDimensionType

from ..models.involvement import Involvement
from ..models.meta import InvolvementEventMeta
from .invitation_full import FullInvitationType
from .profile_with_involvement import ProfileWithInvolvementType


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
        """
        List of people involved in the event, filtered by dimensions.
        """
        request: HttpRequest = info.context

        graphql_check_model(
            Involvement,
            meta.event.scope,
            request,
        )

        return meta.get_people(
            filters=DimensionFilters.from_graphql(filters=filters),
        )

    people = graphene.NonNull(
        graphene.List(
            graphene.NonNull(ProfileWithInvolvementType),
        ),
        filters=graphene.List(DimensionFilterInput, required=False),
        description=normalize_whitespace(resolve_people.__doc__ or ""),
    )

    @staticmethod
    def resolve_dimensions(
        meta: InvolvementEventMeta,
        info,
        # TODO unify naming
        is_list_filter: bool = False,
        is_shown_in_detail: bool = False,
        public_only: bool = True,
        key_dimensions_only: bool = False,
    ):
        """
        `is_list_filter` - only return dimensions that are shown in the list filter.
        `is_shown_in_detail` - only return dimensions that are shown in the detail view.
        If you supply both, you only get their intersection.
        """
        if public_only:
            dimensions = meta.universe.dimensions.filter(is_public=True)
        else:
            graphql_check_instance(
                meta.universe,  # type: ignore
                info,
                field="dimensions",
                app="program_v2",
            )
            dimensions = meta.universe.dimensions.all()

        if is_list_filter:
            dimensions = dimensions.filter(is_list_filter=True)

        if is_shown_in_detail:
            dimensions = dimensions.filter(is_shown_in_detail=True)

        if key_dimensions_only:
            dimensions = dimensions.filter(is_key_dimension=True)

        return dimensions.order_by("order")

    dimensions = graphene.NonNull(
        graphene.List(graphene.NonNull(FullDimensionType)),
        is_list_filter=graphene.Boolean(),
        is_shown_in_detail=graphene.Boolean(),
        public_only=graphene.Boolean(),
        key_dimensions_only=graphene.Boolean(),
        description=normalize_whitespace(resolve_dimensions.__doc__ or ""),
    )
