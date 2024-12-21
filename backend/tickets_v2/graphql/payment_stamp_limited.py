import graphene
from graphene.types.generic import GenericScalar
from graphene_django import DjangoObjectType

from graphql_api.utils import resolve_local_datetime_field

from ..models.payment_stamp import PaymentStamp
from ..optimized_server.models.enums import PaymentProvider, PaymentStampType, PaymentStatus


class LimitedPaymentStampType(DjangoObjectType):
    class Meta:
        model = PaymentStamp
        fields = ("id", "correlation_id", "provider", "status", "data")

    created_at = graphene.NonNull(graphene.DateTime)
    resolve_created_at = resolve_local_datetime_field("timestamp")

    provider = graphene.NonNull(graphene.Enum.from_enum(PaymentProvider))

    # @staticmethod
    # def resolve_provider(payment_stamp, info):
    #     return PaymentProvider(payment_stamp.provider_id)

    status = graphene.NonNull(graphene.Enum.from_enum(PaymentStatus))
    type = graphene.NonNull(graphene.Enum.from_enum(PaymentStampType))

    data = graphene.NonNull(GenericScalar)
