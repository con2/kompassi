import graphene
from django.core.exceptions import SuspiciousOperation
from graphene_django import DjangoObjectType

from core.utils.text_utils import normalize_whitespace

from ..models.meta import TicketsV2EventMeta, TicketsV2ProfileMeta
from ..models.order import OrderOwner
from .order import ProfileOrderType


class TicketsV2EventMetaType(DjangoObjectType):
    class Meta:
        model = TicketsV2EventMeta
        fields = ("provider",)


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
