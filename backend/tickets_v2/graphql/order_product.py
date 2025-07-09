from graphene_pydantic import PydanticObjectType

from ..optimized_server.models.order import OrderProduct


class OrderProductType(PydanticObjectType):
    class Meta:
        model = OrderProduct
