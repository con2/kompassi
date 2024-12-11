import graphene
from django.core.exceptions import SuspiciousOperation
from graphene_django import DjangoObjectType

from access.cbac import graphql_query_cbac_required
from core.utils.text_utils import normalize_whitespace

from ..models.meta import TicketsV2EventMeta, TicketsV2ProfileMeta
from ..models.order import OrderOwner
from ..models.product import Product
from ..models.quota import Quota
from .order import ProfileOrderType
from .product_full import FullProductType
from .quota_full import FullQuotaType


class TicketsV2EventMetaType(DjangoObjectType):
    class Meta:
        model = TicketsV2EventMeta
        fields = ("provider",)

    @graphql_query_cbac_required
    @staticmethod
    def resolve_products(
        meta: TicketsV2EventMeta,
        info,
        superseded_by: int | None = None,
    ):
        """
        Returns products defined for this event.
        Admin oriented view; customers will access product information through /api/tickets-v2.
        If `superseded_by` is provided, only old versions of that product are returned.
        """
        return Product.objects.filter(event=meta.event, superseded_by=superseded_by)

    products = graphene.NonNull(graphene.List(graphene.NonNull(FullProductType)))

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
        return OrderOwner.get_user_orders(meta.person.user_id)

    orders = graphene.NonNull(
        graphene.List(graphene.NonNull(ProfileOrderType)),
        description=normalize_whitespace(resolve_orders.__doc__ or ""),
    )

    @staticmethod
    def resolve_order(meta: TicketsV2ProfileMeta, info, event_slug: str, order_id: str):
        """
        Returns an order of the current user.
        Note that unlinked orders made with the same email address are not returned.
        They need to be linked first (ie. their email confirmed again).
        """
        if info.context.user != meta.person.user:
            raise SuspiciousOperation("User mismatch")
        return OrderOwner.get_user_order(event_slug, order_id, info.context.user.id)

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
        return OrderOwner.have_unclaimed_orders(info.context.user)

    have_unlinked_orders = graphene.NonNull(
        graphene.Boolean,
        description=normalize_whitespace(resolve_have_unlinked_orders.__doc__ or ""),
    )
