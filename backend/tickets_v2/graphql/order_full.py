import graphene

from core.graphql.event_limited import LimitedEventType
from core.utils import normalize_whitespace

from ..models.order import Order
from ..optimized_server.models.enums import PaymentStatus
from .code_limited import LimitedCodeType
from .order_limited import LimitedOrderType
from .order_product import OrderProductType
from .payment_stamp_limited import LimitedPaymentStampType
from .receipt_limited import LimitedReceiptType

PaymentStatusType = graphene.Enum.from_enum(PaymentStatus)


class FullOrderType(LimitedOrderType):
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
            "payment_stamps",
            "receipts",
        )

    event = graphene.NonNull(LimitedEventType)

    @staticmethod
    def resolve_etickets_link(order: Order, info):
        """
        Returns a link at which the admin can view their electronic tickets.
        Returns null if the order does not contain electronic tickets.
        """
        return order.get_etickets_link(info.context)

    etickets_link = graphene.Field(
        graphene.String,
        description=normalize_whitespace(resolve_etickets_link.__doc__ or ""),
    )

    products = graphene.NonNull(
        graphene.List(graphene.NonNull(OrderProductType)),
        description=normalize_whitespace(resolve_etickets_link.__doc__ or ""),
    )

    payment_stamps = graphene.NonNull(
        graphene.List(graphene.NonNull(LimitedPaymentStampType)),
        description="Payment stamps related to this order.",
    )

    receipts = graphene.NonNull(
        graphene.List(graphene.NonNull(LimitedReceiptType)),
        description="Receipts related to this order.",
    )

    codes = graphene.NonNull(
        graphene.List(graphene.NonNull(LimitedCodeType)),
        description="Electronic ticket codes related to this order.",
    )

    @staticmethod
    def resolve_codes(order: Order, info):
        return order.lippukala_codes.all()
