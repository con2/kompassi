from dataclasses import dataclass, field

from lippukala.consts import UNUSED, USED
from lippukala.models import Code

from kompassi.core.models import Event

from .LEGACY_TICKETSV1_product import Product


@dataclass
class ProductHandout:
    """
    Used in the tickets admin reports view. Reports the counts of products handed out
    by product.
    """

    title: str
    handed_out_count: int = field(default=0)
    not_handed_out_count: int = field(default=0)

    @property
    def total_count(self):
        return self.handed_out_count + self.not_handed_out_count

    @classmethod
    def get_product_handouts(cls, event: Event):
        handouts = dict()

        products = Product.objects.filter(event=event, electronic_ticket=True).order_by("ordering", "id")
        for product in products:
            codes = Code.objects.filter(
                order__event=event.slug,
                product_text=product.electronic_ticket_title,
            )

            handout = handouts.setdefault(
                product.electronic_ticket_title,
                cls(product.electronic_ticket_title),
            )
            handout.handed_out_count += codes.filter(status=USED).count()
            handout.not_handed_out_count += codes.filter(status=UNUSED).count()

        return list(handouts.values())
