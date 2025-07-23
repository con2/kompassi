import graphene
from django.http import HttpRequest
from graphene_pydantic import PydanticObjectType

from kompassi.core.graphql.event_limited import LimitedEventType
from kompassi.core.utils import normalize_whitespace

from ..models.order import Order
from ..optimized_server.models.enums import PaymentStatus
from ..optimized_server.models.order import OrderProduct
from .order_limited import LimitedOrderType

PaymentStatusType = graphene.Enum.from_enum(PaymentStatus)


class OrderProductType(PydanticObjectType):
    class Meta:
        model = OrderProduct


class ProfileOrderType(LimitedOrderType):
    class Meta:
        model = Order
        fields = (
            "id",
            "event",
            "order_number",
            "language",
            "first_name",
            "last_name",
            "email",
            "phone",
        )

    event = graphene.NonNull(LimitedEventType)

    @staticmethod
    def resolve_etickets_link(order: Order, info):
        """
        Returns a link at which the user can view their electronic tickets.
        They need to be the owner of the order (or an admin) to access that link.
        Returns null if the order does not contain electronic tickets.
        """
        return order.get_etickets_link(info.context)

    etickets_link = graphene.Field(
        graphene.String,
        description=normalize_whitespace(resolve_etickets_link.__doc__ or ""),
    )

    @staticmethod
    def resolve_products(order: Order, info):
        """
        Contents of the order (also known as order products or order rows).
        """
        return order.products

    products = graphene.NonNull(
        graphene.List(graphene.NonNull(OrderProductType)),
        description=normalize_whitespace(resolve_etickets_link.__doc__ or ""),
    )

    @staticmethod
    def resolve_can_cancel(order: Order, info):
        request: HttpRequest = info.context
        return order.can_be_cancelled_by_owner(request.user)  # type: ignore

    can_cancel = graphene.NonNull(
        graphene.Boolean,
        description=normalize_whitespace(resolve_can_cancel.__doc__ or ""),
    )
