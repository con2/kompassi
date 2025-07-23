import graphene
from django.http import HttpRequest
from graphene_django import DjangoObjectType

from kompassi.graphql_api.utils import resolve_local_datetime_field

from ..models.order import Order
from ..optimized_server.models.enums import PaymentStatus
from ..optimized_server.utils.formatting import format_order_number

PaymentStatusType = graphene.Enum.from_enum(PaymentStatus)


class LimitedOrderType(DjangoObjectType):
    class Meta:
        model = Order
        fields = (
            "id",
            "order_number",
            "language",
            "first_name",
            "last_name",
            "email",
            "phone",
            "display_name",
        )

    created_at = graphene.NonNull(graphene.DateTime)
    resolve_created_at = resolve_local_datetime_field("timestamp")

    @staticmethod
    def resolve_formatted_order_number(order: Order, info):
        return format_order_number(order.order_number)

    formatted_order_number = graphene.NonNull(graphene.String)

    @staticmethod
    def resolve_total_price(order: Order, info):
        return order.cached_price

    total_price = graphene.NonNull(graphene.Decimal)

    @staticmethod
    def resolve_status(order: Order, info):
        return order.cached_status

    status = graphene.NonNull(PaymentStatusType)

    display_name = graphene.NonNull(graphene.String)

    @staticmethod
    def resolve_can_pay(order: Order, info):
        request: HttpRequest = info.context
        return order.can_be_paid_by(request)

    can_pay = graphene.NonNull(graphene.Boolean)
