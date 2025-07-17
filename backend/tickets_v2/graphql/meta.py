import graphene
from django.core.exceptions import SuspiciousOperation
from graphene_django import DjangoObjectType

from access.cbac import graphql_query_cbac_required
from core.utils.text_utils import normalize_whitespace
from dimensions.graphql.dimension_filter_input import DimensionFilterInput

from ..models.meta import TicketsV2EventMeta, TicketsV2ProfileMeta
from ..models.order import Order
from ..models.product import Product
from ..models.quota import Quota
from .order_full import FullOrderType
from .order_profile import ProfileOrderType
from .product_full import FullProductType
from .quota_full import FullQuotaType


class TicketsV2EventMetaType(DjangoObjectType):
    class Meta:
        model = TicketsV2EventMeta
        fields = ("provider_id",)

    @graphql_query_cbac_required
    @staticmethod
    def resolve_products(meta: TicketsV2EventMeta, info):
        """
        Returns products defined for this event.
        Admin oriented view; customers will access product information through /api/tickets-v2.
        """
        return Product.objects.filter(
            event=meta.event,
            superseded_by=None,
        ).order_by("ordering")

    products = graphene.NonNull(
        graphene.List(graphene.NonNull(FullProductType)),
        description=normalize_whitespace(resolve_products.__doc__ or ""),
    )

    @graphql_query_cbac_required
    @staticmethod
    def resolve_product(meta: TicketsV2EventMeta, info, id: str):
        """
        Returns a product defined for this event.
        Admin oriented view; customers will access product information through /api/tickets-v2.
        """
        return (
            Product.objects.filter(
                event=meta.event,
                id=id,
            )
            .select_related("event", "superseded_by")
            .first()
        )

    product = graphene.NonNull(
        FullProductType,
        description=normalize_whitespace(resolve_product.__doc__ or ""),
        id=graphene.String(required=True),
    )

    @graphql_query_cbac_required
    @staticmethod
    def resolve_quotas(
        meta: TicketsV2EventMeta,
        info,
    ):
        """
        Returns quotas defined for this event.
        Admin oriented view; customers will access quota information through /api/tickets-v2.
        """
        return Quota.objects.filter(event=meta.event)

    quotas = graphene.NonNull(graphene.List(graphene.NonNull(FullQuotaType)))

    @graphql_query_cbac_required
    @staticmethod
    def resolve_quota(meta: TicketsV2EventMeta, info, id: int):
        """
        Returns a quota defined for this event.
        Admin oriented view; customers will access product information through /api/tickets-v2.
        """
        return Quota.objects.filter(event=meta.event, id=id).first()

    quota = graphene.NonNull(
        FullQuotaType,
        description=normalize_whitespace(resolve_quota.__doc__ or ""),
        id=graphene.Int(required=True),
    )

    @graphql_query_cbac_required
    @staticmethod
    def resolve_orders(
        meta: TicketsV2EventMeta,
        info,
        filters: list[DimensionFilterInput] | None = None,
        search: str = "",
        return_none: bool = False,
    ):
        """
        Returns orders made to this event.
        Admin oriented view; customers will access order information through `profile.tickets`.
        """
        if return_none:
            return Order.objects.none()

        return Order.filter_orders(
            Order.objects.filter(event=meta.event),
            filters=filters,
            search=search,
        ).order_by("-id")

    orders = graphene.NonNull(
        graphene.List(graphene.NonNull(FullOrderType)),
        filters=graphene.List(DimensionFilterInput),
        search=graphene.String(),
        return_none=graphene.Boolean(default_value=False),
        description=normalize_whitespace(resolve_orders.__doc__ or ""),
    )

    @graphql_query_cbac_required
    @staticmethod
    def resolve_count_total_orders(meta: TicketsV2EventMeta, info):
        """
        Returns the total number of orders made to this event.
        Admin oriented view; customers will access order information through `profile.tickets`.
        """
        return Order.objects.filter(event=meta.event).count()

    count_total_orders = graphene.NonNull(
        graphene.Int,
        description=normalize_whitespace(resolve_count_total_orders.__doc__ or ""),
    )

    @graphql_query_cbac_required
    @staticmethod
    def resolve_order(meta: TicketsV2EventMeta, info, id: str):
        """
        Returns an order made to this event.
        Admin oriented view; customers will access order information through `profile.tickets`.
        """
        return Order.objects.filter(event=meta.event, id=id).first()

    order = graphene.Field(
        FullOrderType,
        id=graphene.String(required=True),
        description=normalize_whitespace(resolve_orders.__doc__ or ""),
    )


class TicketsV2ProfileMetaType(graphene.ObjectType):
    @staticmethod
    def resolve_orders(meta: TicketsV2ProfileMeta, info):
        """
        Returns the orders of the current user.
        Note that unlinked orders made with the same email address are not returned.
        They need to be linked first (ie. their email confirmed again).
        """
        if info.context.user != meta.person.user:
            raise SuspiciousOperation("User mismatch")

        return Order.objects.filter(owner=meta.person.user)

    orders = graphene.NonNull(
        graphene.List(graphene.NonNull(ProfileOrderType)),
        description=normalize_whitespace(resolve_orders.__doc__ or ""),
    )

    @staticmethod
    def resolve_order(meta: TicketsV2ProfileMeta, info, event_slug: str, id: str):
        """
        Returns an order of the current user.
        Note that unlinked orders made with the same email address are not returned.
        They need to be linked first (ie. their email confirmed again).
        """
        if info.context.user != meta.person.user:
            raise SuspiciousOperation("User mismatch")

        return Order.objects.filter(
            event__slug=event_slug,
            id=id,
            owner=meta.person.user,
        ).first()

    order = graphene.Field(
        ProfileOrderType,
        event_slug=graphene.String(required=True),
        id=graphene.String(required=True),
    )

    @staticmethod
    def resolve_have_unlinked_orders(meta: TicketsV2ProfileMeta, info):
        """
        Returns true if the user has unlinked orders made with the same email address.
        These orders can be linked to the user account by verifying the email address again.
        """
        if info.context.user != meta.person.user:
            raise SuspiciousOperation("User mismatch")

        return Order.objects.filter(
            owner=None,
            email=meta.person.email,
        ).exists()

    have_unlinked_orders = graphene.NonNull(
        graphene.Boolean,
        description=normalize_whitespace(resolve_have_unlinked_orders.__doc__ or ""),
    )
