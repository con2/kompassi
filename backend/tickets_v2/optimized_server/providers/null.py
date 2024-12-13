from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, ClassVar

from ..excs import ProviderCannot
from ..models.enums import PaymentProvider
from ..models.payment_stamp import PaymentStamp

if TYPE_CHECKING:
    from ..models.event import Event
    from ..models.order import CreateOrderRequest, CreateOrderResult, OrderWithCustomer


@dataclass
class NullProvider:
    event: Event

    provider_id: ClassVar[PaymentProvider] = PaymentProvider.NONE

    def prepare_for_new_order(
        self,
        _order: CreateOrderRequest,
        result: CreateOrderResult,
    ) -> tuple[None, PaymentStamp]:
        if result.total_price != 0:
            raise ProviderCannot("Null provider cannot handle non-zero price orders")

        return None, PaymentStamp.for_zero_price_order(
            self.event.id,
            result.order_id,
            self.provider_id,
        )

    def prepare_for_existing_order(
        self,
        order: OrderWithCustomer,
    ):
        raise ProviderCannot("Null provider cowardly refuses to handle existing orders")
