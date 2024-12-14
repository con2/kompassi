import graphene
from graphene_django import DjangoObjectType

from graphql_api.utils import resolve_local_datetime_field

from ..models.receipt import Receipt
from ..optimized_server.models.enums import ReceiptStatus, ReceiptType


class LimitedReceiptType(DjangoObjectType):
    class Meta:
        model = Receipt
        fields = ("email", "status", "correlation_id")

    created_at = graphene.NonNull(graphene.DateTime)
    resolve_created_at = resolve_local_datetime_field("timestamp")

    status = graphene.NonNull(graphene.Enum.from_enum(ReceiptStatus))
    type = graphene.NonNull(graphene.Enum.from_enum(ReceiptType))
