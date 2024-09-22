from datetime import timedelta
from decimal import Decimal

import pytest
from django.utils.timezone import now

from core.models.event import Event
from tickets_v2.models.meta import TicketsV2EventMeta
from tickets_v2.models.product import Product
from tickets_v2.models.quota import Quota
from tickets_v2.models.ticket import Ticket
from tickets_v2.optimized_server.models.customer import Customer
from tickets_v2.optimized_server.models.order import Order


@pytest.mark.django_db
@pytest.mark.xfail
def test_reserve():
    """
    XFAIL Pytest-django does something strange with transactions, causing this test to fail.
    """
    event, _ = Event.get_or_create_dummy()

    (admin_group,) = TicketsV2EventMeta.get_or_create_groups(event, ["admins"])
    meta = TicketsV2EventMeta.objects.create(
        event=event,
        admin_group=admin_group,
    )

    meta.ensure_partitions()

    friday_quota = Quota.objects.create(
        event=event,
        name="Perjantai",
    )
    friday_quota.set_quota(5500)

    saturday_quota = Quota.objects.create(
        event=event,
        name="Lauantai",
    )
    saturday_quota.set_quota(5500)

    sunday_quota = Quota.objects.create(
        event=event,
        name="Sunnuntai",
    )
    sunday_quota.set_quota(5500)

    available_from = now()
    available_until = now() + timedelta(days=1)

    friday_quota.products.create(
        event=event,
        title="Perjantailippu",
        price=Decimal("25.00"),
        available_from=available_from,
        available_until=available_until,
    )
    saturday_quota.products.create(
        event=event,
        title="Lauantailippu",
        price=Decimal("40.00"),
        available_from=available_from,
        available_until=available_until,
    )
    sunday_quota.products.create(
        event=event,
        title="Sunnuntailippu",
        price=Decimal("35.00"),
        available_from=available_from,
        available_until=available_until,
    )

    weekend_ticket = Product.objects.create(
        event=event,
        title="Viikonloppulippu",
        price=Decimal("50.00"),
        available_from=available_from,
        available_until=available_until,
    )

    weekend_ticket.quotas.set([friday_quota, saturday_quota, sunday_quota])

    order_dto = Order(
        customer=Customer(
            firstName="John",
            lastName="Doe",
            email="john.doe@example.com",
            phone="+358505551234",
        ),
        products={
            weekend_ticket.id: 1,
        },
    )

    order_id = order_dto.save_django(event.id)

    tickets = Ticket.objects.filter(event=event, order_id=order_id)
    assert len(tickets) == 3
