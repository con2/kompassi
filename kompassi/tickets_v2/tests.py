import json
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from functools import cached_property
from types import SimpleNamespace
from typing import Any, Literal
from uuid import UUID, uuid4

import pydantic
import pytest
import requests
from django.core import mail

from kompassi.core.models.event import Event
from kompassi.tickets_v2.graphql.mutations.confirm_order_cancellation import ConfirmOrderCancellation
from kompassi.tickets_v2.graphql.mutations.request_order_cancellation import RequestOrderCancellation
from kompassi.tickets_v2.models.meta import TicketsV2EventMeta
from kompassi.tickets_v2.models.order import Order
from kompassi.tickets_v2.models.order_cancellation_token import OrderCancellationToken
from kompassi.tickets_v2.models.payment_stamp import PaymentStamp
from kompassi.tickets_v2.models.product import Product
from kompassi.tickets_v2.models.receipt import PendingReceipt
from kompassi.tickets_v2.optimized_server.models.api import CreateOrderResponse, GetOrderResponse, GetProductsResponse
from kompassi.tickets_v2.optimized_server.models.customer import Customer
from kompassi.tickets_v2.optimized_server.models.enums import (
    PaymentProvider,
    PaymentStampType,
    PaymentStatus,
)
from kompassi.tickets_v2.optimized_server.models.order import CreateOrderRequest, OrderProduct, VatBreakdownLine
from kompassi.tickets_v2.optimized_server.providers.paytrail import PaymentCallback, PaytrailStatus
from kompassi.tickets_v2.optimized_server.utils.formatting import format_vat_rate
from kompassi.tickets_v2.optimized_server.utils.paytrail_hmac import calculate_hmac
from kompassi.tickets_v2.optimized_server.utils.uuid7 import uuid7
from kompassi.tickets_v2.reports.vat_by_month import VatByMonth

PAYTRAIL_TEST_ACCOUNT = "375917"
PAYTRAIL_TEST_SECRET = "SAIPPUAKAUPPIAS"


def test_paytrail_hmac():
    headers = {
        "checkout-account": PAYTRAIL_TEST_ACCOUNT,
        "checkout-algorithm": "sha256",
        "checkout-method": "POST",
        "checkout-nonce": "564635208570151",
        "checkout-timestamp": "2018-07-06T10:01:31.904Z",
    }

    body = {
        "stamp": "unique-identifier-for-merchant",
        "reference": "3759170",
        "amount": 1525,
        "currency": "EUR",
        "language": "FI",
        "items": [
            {
                "unitPrice": 1525,
                "units": 1,
                "vatPercentage": 24,
                "productCode": "#1234",
                "deliveryDate": "2018-09-01",
            }
        ],
        "customer": {"email": "test.customer@example.com"},
        "redirectUrls": {
            "success": "https://ecom.example.com/cart/success",
            "cancel": "https://ecom.example.com/cart/cancel",
        },
    }

    # encoded here without spaces in the output to match known hmac from examples
    # https://checkoutfinland.github.io/psp-api/#/examples?id=hmac-calculation-node-js
    body = json.dumps(body, separators=(",", ":"))

    assert (
        calculate_hmac(PAYTRAIL_TEST_SECRET, headers, body)
        == "3708f6497ae7cc55a2e6009fc90aa10c3ad0ef125260ee91b19168750f6d74f6"
    )


class TicketsV2Client:
    """
    Test client for the Tickets V2 API (Optimized Server).
    """

    event_slug: str
    api_url: str

    def __init__(self, event_slug: str, api_url: str = "http://localhost:7998/api/tickets-v2"):
        self.event_slug = event_slug
        self.api_url = api_url

    @cached_property
    def event(self) -> Event:
        return Event.objects.get(slug=self.event_slug)

    def _get_url(self, *path_components: Any):
        parts = [
            self.api_url,
            self.event_slug,
            *path_components,
            # trailing slash to avoid 307 redirect from Starlette
            "",
        ]
        return "/".join(str(part) for part in parts)

    def _get(self, *path_components: Any, query: dict[str, Any] | None = None):
        response = requests.get(self._get_url(*path_components), params=query)
        response.raise_for_status()
        return response.json()

    def _post(self, *path_components: Any, body: pydantic.BaseModel | None = None):
        response = requests.post(
            self._get_url(*path_components),
            json=body.model_dump(mode="json", by_alias=True) if body is not None else None,
        )
        response.raise_for_status()
        return response.json()

    def get_products(self):
        return GetProductsResponse.model_validate(self._get("products"))

    def create_order(self, request: CreateOrderRequest) -> CreateOrderResponse:
        # TODO mock Paytrail API use (currently actually calls Paytrail with test merchant)
        return CreateOrderResponse.model_validate(self._post("orders", body=request))

    def get_order(self, order_id: UUID):
        return GetOrderResponse.model_validate(self._get("orders", order_id))

    def pay(self, order_id: UUID) -> CreateOrderResponse:
        # TODO mock Paytrail API use (currently actually calls Paytrail with test merchant)
        return CreateOrderResponse.model_validate(self._post("orders", order_id, "payment", body=None))

    def payment_callback(
        self,
        order_id: UUID,
        status: PaytrailStatus,
        mode: Literal["redirect", "callback"] = "redirect",
    ):
        """
        NOTE: Always simulates redirect or callback for the *latest* payment attempt for now.
        If you need to test multiple concurrent payment attempts, need to select the correct
        payment stamp by `data["reference"]` or similar.
        """
        query = PaymentCallback(
            account=PAYTRAIL_TEST_ACCOUNT,
            algorithm="sha256",
            # NOTE: abusing the fact the implementation does not check the sum here
            amount_cents=0,
            # NOTE: may break if we harden the way stamps are handled to check that stamps match
            stamp=uuid7(),
            reference="impl does not care about reference",
            transaction_id=str(uuid4()),
            status=status,
            provider_name="dummy",
            signature="",
        ).model_dump(mode="json", by_alias=True)
        signature = calculate_hmac(PAYTRAIL_TEST_SECRET, query)
        query["signature"] = signature

        # can't use _get because body is not JSON
        response = requests.get(
            self._get_url("orders", order_id, mode),
            params=query,
            allow_redirects=False,
        )

        match mode:
            case "redirect":
                assert response.status_code == 303
                assert response.headers["location"]
            case "callback":
                assert response.status_code == 200
                assert response.text == ""
            case _:
                raise ValueError(f"Unknown mode: {mode}")


class GraphQLClient:
    event_slug: str
    api_url: str

    def __init__(self, event_slug: str, api_url: str = "http://localhost:8000/graphql"):
        self.event_slug = event_slug
        self.api_url = api_url

    def _query(self, query: str, variables: dict[str, Any] | None = None):
        if variables is None:
            variables = {}

        response = requests.post(self.api_url, json={"query": query, "variables": variables})
        response.raise_for_status()
        return response.json()

    def _mutate(self, mutation: str, variables: dict[str, Any] | None = None):
        if variables is None:
            variables = {}

        response = requests.post(self.api_url, json={"mutation": mutation, "variables": variables})
        response.raise_for_status()
        return response.json()


@pytest.fixture
def tickets_v2_client() -> TicketsV2Client:
    return TicketsV2Client("tracon2025")


@pytest.fixture
def graphql_client() -> GraphQLClient:
    return GraphQLClient("tracon2025")


@pytest.mark.integration_test
def test_make_order(tickets_v2_client: TicketsV2Client):
    """
    Exercises the whole order process through the API.
    """
    products = tickets_v2_client.get_products()
    assert len(products.products) > 0

    order_request = CreateOrderRequest(
        products={products.products[-1].id: 3},
        customer=Customer(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
        ),
        language="en",
    )

    order_response = tickets_v2_client.create_order(order_request)
    assert order_response.status == PaymentStatus.PENDING
    assert order_response.payment_redirect

    # first payment attempt cancelled
    tickets_v2_client.payment_callback(order_response.order_id, PaytrailStatus.FAIL)

    # user redirected to order page
    get_order_response = tickets_v2_client.get_order(order_response.order_id)
    assert get_order_response.order.status == PaymentStatus.FAILED

    # second payment attempt successful
    pay_response = tickets_v2_client.pay(order_response.order_id)
    assert pay_response.status == PaymentStatus.PENDING
    assert pay_response.payment_redirect

    # let's do it with a callback just to exercise that, too
    tickets_v2_client.payment_callback(pay_response.order_id, PaytrailStatus.OK, "callback")

    # user redirected to order page again
    get_order_response = tickets_v2_client.get_order(order_response.order_id)
    assert get_order_response.order.status == PaymentStatus.PAID

    # the dev environment event has cancellation_period_days = 0 (the default),
    # so customer self-service cancellation is not offered
    assert get_order_response.order.can_request_cancellation is False
    assert get_order_response.order.cancellation_deadline is None


# ---------------------------------------------------------------------------
# VAT formatting / breakdown unit tests
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "rate,expected_en,expected_fi",
    [
        (Decimal("0"), "0", "0"),
        (Decimal("0.00"), "0", "0"),
        (Decimal("10.00"), "10", "10"),
        (Decimal("13.50"), "13.5", "13,5"),
        (Decimal("14.00"), "14", "14"),
        (Decimal("25.50"), "25.5", "25,5"),
        (Decimal("0.50"), "0.5", "0,5"),
        (Decimal("99.99"), "99.99", "99,99"),
    ],
)
def test_format_vat_rate(rate, expected_en, expected_fi):
    """
    Regression test: Decimal('10.00').normalize() returns Decimal('1E+1'),
    so a naive str(rate.normalize()) implementation would render '1E+1'
    instead of '10' in receipts.
    """
    assert format_vat_rate(rate, "en") == expected_en
    assert format_vat_rate(rate, "fi") == expected_fi
    # Swedish uses the same decimal separator as Finnish
    assert format_vat_rate(rate, "sv") == expected_fi


def test_vat_breakdown_empty():
    assert VatBreakdownLine.from_order_products([]) == []


def test_vat_breakdown_sums_per_rate_and_returns_sorted():
    products = [
        OrderProduct(title="A", price=Decimal("125.50"), quantity=2, vat_percentage=Decimal("25.50")),
        OrderProduct(title="B", price=Decimal("114.00"), quantity=1, vat_percentage=Decimal("14.00")),
        OrderProduct(title="C", price=Decimal("125.50"), quantity=1, vat_percentage=Decimal("25.50")),
    ]
    breakdown = VatBreakdownLine.from_order_products(products)

    # Two rates present, sorted ascending.
    assert [line.rate for line in breakdown] == [Decimal("14.00"), Decimal("25.50")]

    # 14% line: 1 * 114 = 114 gross, VAT = 114 * 14/114 = 14
    assert breakdown[0].gross == Decimal("114.00")
    assert breakdown[0].vat == Decimal("14.00")
    assert breakdown[0].net == Decimal("100.00")

    # 25.5% line: 3 * 125.50 = 376.50 gross, VAT = 376.50 * 25.5/125.5 = 76.50
    assert breakdown[1].gross == Decimal("376.50")
    assert breakdown[1].vat == Decimal("76.50")
    assert breakdown[1].net == Decimal("300.00")


def test_vat_breakdown_zero_rate_kept():
    """
    The breakdown itself preserves 0% rates (used in receipts to itemize
    zero-rated lines). Filtering of 0% is the VAT-by-month report's concern.
    """
    products = [
        OrderProduct(title="Free", price=Decimal("5.00"), quantity=1, vat_percentage=Decimal("0")),
    ]
    breakdown = VatBreakdownLine.from_order_products(products)
    assert len(breakdown) == 1
    assert breakdown[0].rate == Decimal("0")
    assert breakdown[0].gross == Decimal("5.00")
    assert breakdown[0].vat == Decimal("0.00")
    assert breakdown[0].net == Decimal("5.00")


# ---------------------------------------------------------------------------
# VAT-by-month report integration tests
# ---------------------------------------------------------------------------


def _make_order(
    event: Event,
    when: datetime,
    product_data: dict[int, int],
    status: PaymentStatus = PaymentStatus.PAID,
    total_price: Decimal = Decimal(0),
) -> UUID:
    """
    Insert a tickets_v2_order row directly via SQL.

    Bypasses the ORM because tickets_v2_order.order_number is GENERATED ALWAYS
    AS IDENTITY at the DB layer, so Django can't INSERT through the column;
    the production code path goes through create_order.sql for the same reason.
    Returns the order id.
    """
    from django.db import connection

    order_id = uuid7(when)
    with connection.cursor() as cursor:
        cursor.execute(
            """
            insert into tickets_v2_order
                (id, event_id, cached_status, cached_price, language, product_data,
                 first_name, last_name, email, phone)
            values
                (%s, %s, %s, %s, %s, %s::jsonb, %s, %s, %s, %s)
            """,
            [
                str(order_id),
                event.id,
                status.value,
                str(total_price),
                "en",
                json.dumps({str(pid): qty for pid, qty in product_data.items()}),
                "Test",
                "Customer",
                "test@example.com",
                "",
            ],
        )
    return order_id


@pytest.fixture
def vat_report_event(db):
    event, _ = Event.get_or_create_dummy(name="VAT report test event")
    # Sanity-check the timezone the report relies on for month bucketing.
    assert event.timezone_name == "Europe/Helsinki"
    Order.ensure_partition(event)
    return event


@pytest.mark.django_db
def test_vat_by_month_report_empty(vat_report_event: Event):
    """No orders → no rows, but the report still renders with a month column."""
    report = VatByMonth.report(vat_report_event, "en")
    assert report.slug == "vat_by_month"
    assert report.rows == []
    assert [c.slug for c in report.columns] == ["month", "total"]
    assert report.total_row is None  # has_total_row is False when there are no rows


@pytest.mark.django_db
def test_vat_by_month_report_basic(vat_report_event: Event):
    """
    Multiple VAT rates across multiple months, with an unpaid order and a
    zero-VAT order included to verify both filters.
    """
    # Prices chosen so VAT comes out to clean Decimals:
    #  - 125.50 @ 25.5% → VAT/unit = 125.50 * 25.5 / 125.5 = 25.50
    #  - 114.00 @ 14%   → VAT/unit = 114.00 * 14 / 114   = 14.00
    standard = Product.objects.create(
        event=vat_report_event,
        title="Standard product",
        description="",
        price=Decimal("125.50"),
        vat_percentage=Decimal("25.50"),
    )
    reduced = Product.objects.create(
        event=vat_report_event,
        title="Food product",
        description="",
        price=Decimal("114.00"),
        vat_percentage=Decimal("14.00"),
    )
    zero_rated = Product.objects.create(
        event=vat_report_event,
        title="Free product",
        description="",
        price=Decimal("5.00"),
        vat_percentage=Decimal("0"),
    )

    # Jan 2026 (Helsinki): 1× standard → 25.5% column = 25.50
    _make_order(vat_report_event, datetime(2026, 1, 15, 12, 0, tzinfo=UTC), {standard.id: 1})
    # Feb 2026 (Helsinki): 1× standard + 2× reduced → 25.5% = 25.50, 14% = 28.00
    _make_order(vat_report_event, datetime(2026, 2, 10, 12, 0, tzinfo=UTC), {standard.id: 1, reduced.id: 2})
    # Unpaid Feb order (must be excluded)
    _make_order(
        vat_report_event,
        datetime(2026, 2, 20, 12, 0, tzinfo=UTC),
        {standard.id: 1},
        status=PaymentStatus.PENDING,
    )
    # Paid zero-VAT Feb order (must be excluded)
    _make_order(vat_report_event, datetime(2026, 2, 25, 12, 0, tzinfo=UTC), {zero_rated.id: 1})

    report = VatByMonth.report(vat_report_event, "en")

    column_slugs = [c.slug for c in report.columns]
    assert column_slugs == ["month", "vat_14.00", "vat_25.50", "total"]

    assert len(report.rows) == 2
    jan, feb = report.rows
    assert jan == ["2026-01", 0.00, 25.50, 25.50]
    assert feb == ["2026-02", 28.00, 25.50, 53.50]

    # Total row sums each column (skipping the month column, which is total_by=NONE).
    assert report.total_row is not None
    month_label, total_14, total_25_5, grand_total = report.total_row
    assert month_label == "Total"
    assert total_14 == pytest.approx(28.00)
    assert total_25_5 == pytest.approx(51.00)
    assert grand_total == pytest.approx(79.00)


@pytest.mark.django_db
def test_vat_by_month_report_refund_does_not_change_history(vat_report_event: Event):
    """
    Once an order has been paid, its VAT belongs to the month of the sale even if
    the order is later refunded — the VAT for that month may already have been
    filed, so the report must not change retroactively. (The footer tells the
    reader that refunds are not subtracted.)
    """
    product = Product.objects.create(
        event=vat_report_event,
        title="Standard",
        description="",
        price=Decimal("125.50"),
        vat_percentage=Decimal("25.50"),
    )

    _make_order(vat_report_event, datetime(2026, 1, 15, 12, 0, tzinfo=UTC), {product.id: 1})
    for status in (
        PaymentStatus.REFUND_REQUESTED,
        PaymentStatus.REFUND_FAILED,
        PaymentStatus.REFUNDED,
    ):
        _make_order(vat_report_event, datetime(2026, 1, 20, 12, 0, tzinfo=UTC), {product.id: 1}, status=status)

    report = VatByMonth.report(vat_report_event, "en")
    assert report.rows == [["2026-01", 4 * 25.50, 4 * 25.50]]


@pytest.mark.django_db
def test_vat_by_month_report_timezone_boundary(vat_report_event: Event):
    """
    An order at 23:30 UTC on Jan 31 falls on Feb 1 in Helsinki (UTC+2),
    so the report should bucket it in February.
    """
    product = Product.objects.create(
        event=vat_report_event,
        title="Standard",
        description="",
        price=Decimal("125.50"),
        vat_percentage=Decimal("25.50"),
    )
    # UTC moment that is already in February when projected into Europe/Helsinki.
    _make_order(vat_report_event, datetime(2026, 1, 31, 23, 30, tzinfo=UTC), {product.id: 1})

    report = VatByMonth.report(vat_report_event, "en")
    assert [row[0] for row in report.rows] == ["2026-02"]


@pytest.mark.django_db
def test_vat_by_month_report_localized_titles(vat_report_event: Event):
    """Column titles for VAT rates follow the requested locale's separator."""
    Product.objects.create(
        event=vat_report_event,
        title="Standard",
        description="",
        price=Decimal("125.50"),
        vat_percentage=Decimal("25.50"),
    )
    _make_order(
        vat_report_event,
        datetime(2026, 3, 15, 12, 0, tzinfo=UTC),
        {vat_report_event.products.get().id: 1},
    )

    en_report = VatByMonth.report(vat_report_event, "en")
    fi_report = VatByMonth.report(vat_report_event, "fi")
    # The Column.title is a dict that resolve_localized_field picks from at GraphQL
    # serialization time; we just verify both locales are populated correctly.
    vat_col_en = next(c for c in en_report.columns if c.slug == "vat_25.50")
    vat_col_fi = next(c for c in fi_report.columns if c.slug == "vat_25.50")
    assert vat_col_en.title["en"] == "25.5%"
    assert vat_col_fi.title["fi"] == "25,5%"


# ---------------------------------------------------------------------------
# Order filtering tests
# ---------------------------------------------------------------------------


@pytest.mark.django_db
def test_filter_orders_by_product_includes_superseded_versions(vat_report_event: Event):
    """
    Editing a product creates a new revision (superseded_by), but old orders keep
    referencing the old product id in product_data. Filtering orders by the
    current product id must still return orders made against an older, superseded
    version of that product (see update_product.py:137-155 for how revisions are created).
    """
    old_product = Product.objects.create(
        event=vat_report_event,
        title="Seminar ticket",
        description="",
        price=Decimal("10.00"),
        vat_percentage=Decimal("25.50"),
    )
    old_order_id = _make_order(vat_report_event, datetime(2026, 1, 1, 12, 0, tzinfo=UTC), {old_product.id: 1})

    new_product = Product.objects.create(
        event=vat_report_event,
        title="Seminar ticket",
        description="",
        price=Decimal("12.00"),
        vat_percentage=Decimal("25.50"),
    )
    old_product.superseded_by = new_product
    old_product.save()
    new_order_id = _make_order(vat_report_event, datetime(2026, 2, 1, 12, 0, tzinfo=UTC), {new_product.id: 1})

    filters = [SimpleNamespace(dimension="product", values=[str(new_product.id)])]
    filtered_order_ids = set(
        Order.filter_orders(Order.objects.filter(event=vat_report_event), filters=filters).values_list("id", flat=True)
    )

    assert filtered_order_ids == {old_order_id, new_order_id}


# ---------------------------------------------------------------------------
# Customer self-service cancellation tests
# ---------------------------------------------------------------------------


def _add_provider_paid_stamp(event: Event, order_id: UUID):
    """
    Simulate a successful payment via a payment provider. The payment stamp
    trigger updates the cached status of the order to PAID.
    """
    PaymentStamp(
        event=event,
        order_id=order_id,
        correlation_id=uuid7(),
        provider_id=PaymentProvider.PAYTRAIL,
        type=PaymentStampType.PAYMENT_CALLBACK,
        status=PaymentStatus.PAID,
        data={},
    ).save()


def _request_input(event: Event, order_id: UUID):
    return SimpleNamespace(event_slug=event.slug, order_id=str(order_id))


def _confirm_input(event: Event, order_id: UUID, code: str):
    return SimpleNamespace(event_slug=event.slug, order_id=str(order_id), code=code)


@pytest.fixture
def cancellation_event(db):
    from kompassi.event_log_v2.models.entry import Entry

    event, _ = Event.get_or_create_dummy(name="Cancellation test event")
    (admin_group,) = TicketsV2EventMeta.get_or_create_groups(event, ["admins"])
    meta, _ = TicketsV2EventMeta.objects.update_or_create(
        event=event,
        defaults=dict(
            admin_group=admin_group,
            contact_email="Test Ticket Sales <tickets@example.com>",
            cancellation_period_days=14,
        ),
    )
    meta.ensure_partitions()
    Entry.ensure_partitions()
    return event


def _get_order(event: Event, order_id: UUID) -> Order:
    return Order.objects.get(event=event, id=order_id)


@pytest.mark.django_db
def test_can_be_cancelled_by_customer_zero_price(cancellation_event: Event):
    event = cancellation_event
    now = datetime.now(UTC)

    order_id = _make_order(event, now, {}, status=PaymentStatus.PAID)
    order = _get_order(event, order_id)

    # event starts in 60 days, so the deadline comes from the cancellation period
    assert order.cancellation_deadline == order.timestamp + timedelta(days=14)
    assert order.can_be_cancelled_by_customer()


@pytest.mark.django_db
def test_can_be_cancelled_by_customer_provider_paid(cancellation_event: Event):
    event = cancellation_event
    now = datetime.now(UTC)

    order_id = _make_order(event, now, {}, status=PaymentStatus.PENDING, total_price=Decimal("10.00"))
    _add_provider_paid_stamp(event, order_id)

    order = _get_order(event, order_id)
    assert order.status == PaymentStatus.PAID
    assert order.can_be_cancelled_by_customer()


@pytest.mark.django_db
def test_can_be_cancelled_by_customer_manually_paid(cancellation_event: Event):
    """
    A paid order with money paid outside a payment provider (eg. marked as paid
    by an admin) cannot be self-service cancelled because the money cannot be
    automatically refunded.
    """
    event = cancellation_event
    now = datetime.now(UTC)

    order_id = _make_order(event, now, {}, status=PaymentStatus.PAID, total_price=Decimal("10.00"))
    assert not _get_order(event, order_id).can_be_cancelled_by_customer()


@pytest.mark.django_db
def test_can_be_cancelled_by_customer_period_expired(cancellation_event: Event):
    event = cancellation_event
    when = datetime.now(UTC) - timedelta(days=15)

    order_id = _make_order(event, when, {}, status=PaymentStatus.PAID)
    assert not _get_order(event, order_id).can_be_cancelled_by_customer()


@pytest.mark.django_db
def test_can_be_cancelled_by_customer_event_started(cancellation_event: Event):
    event = cancellation_event
    event.start_time = datetime.now(UTC) - timedelta(hours=1)
    event.save(update_fields=["start_time"])

    order_id = _make_order(event, datetime.now(UTC), {}, status=PaymentStatus.PAID)
    assert not _get_order(event, order_id).can_be_cancelled_by_customer()


@pytest.mark.django_db
def test_can_be_cancelled_by_customer_no_start_time(cancellation_event: Event):
    event = cancellation_event
    event.start_time = None
    event.end_time = None
    event.save(update_fields=["start_time", "end_time"])

    order_id = _make_order(event, datetime.now(UTC), {}, status=PaymentStatus.PAID)
    order = _get_order(event, order_id)
    assert order.cancellation_deadline == order.timestamp + timedelta(days=14)
    assert order.can_be_cancelled_by_customer()


@pytest.mark.django_db
def test_can_be_cancelled_by_customer_disabled(cancellation_event: Event):
    event = cancellation_event
    meta = TicketsV2EventMeta.objects.get(event=event)
    meta.cancellation_period_days = 0
    meta.save(update_fields=["cancellation_period_days"])

    order_id = _make_order(event, datetime.now(UTC), {}, status=PaymentStatus.PAID)
    order = _get_order(event, order_id)
    assert order.cancellation_deadline is None
    assert not order.can_be_cancelled_by_customer()


@pytest.mark.django_db
@pytest.mark.parametrize(
    "status",
    [
        PaymentStatus.NOT_STARTED,
        PaymentStatus.PENDING,
        PaymentStatus.FAILED,
        PaymentStatus.CANCELLED,
        PaymentStatus.REFUND_REQUESTED,
        PaymentStatus.REFUND_FAILED,
        PaymentStatus.REFUNDED,
    ],
)
def test_can_be_cancelled_by_customer_wrong_status(cancellation_event: Event, status: PaymentStatus):
    event = cancellation_event
    order_id = _make_order(event, datetime.now(UTC), {}, status=status)
    assert not _get_order(event, order_id).can_be_cancelled_by_customer()


@pytest.mark.django_db
def test_request_order_cancellation(cancellation_event: Event):
    event = cancellation_event
    order_id = _make_order(event, datetime.now(UTC), {}, status=PaymentStatus.PAID)

    RequestOrderCancellation.mutate(None, None, _request_input(event, order_id))

    token = OrderCancellationToken.objects.get(event=event, order_id=order_id, state="valid")
    assert len(mail.outbox) == 1
    message = mail.outbox[0]
    assert token.confirmation_url in message.body
    assert message.to == ["Test Customer <test@example.com>"]
    assert message.reply_to == ["Test Ticket Sales <tickets@example.com>"]

    # requesting again right away is throttled (email bombing prevention)
    with pytest.raises(ValueError):
        RequestOrderCancellation.mutate(None, None, _request_input(event, order_id))
    token.refresh_from_db()
    assert token.state == "valid"
    assert len(mail.outbox) == 1

    # once the throttle period has passed, requesting again
    # revokes the previous token and sends a new one
    OrderCancellationToken.objects.filter(pk=token.pk).update(created_at=datetime.now(UTC) - timedelta(minutes=2))
    RequestOrderCancellation.mutate(None, None, _request_input(event, order_id))
    token.refresh_from_db()
    assert token.state == "revoked"
    assert OrderCancellationToken.objects.filter(event=event, order_id=order_id, state="valid").count() == 1
    assert len(mail.outbox) == 2


@pytest.mark.django_db
def test_request_order_cancellation_ineligible(cancellation_event: Event):
    event = cancellation_event
    order_id = _make_order(event, datetime.now(UTC), {}, status=PaymentStatus.PENDING)

    with pytest.raises(ValueError):
        RequestOrderCancellation.mutate(None, None, _request_input(event, order_id))

    assert not OrderCancellationToken.objects.filter(event=event, order_id=order_id).exists()
    assert len(mail.outbox) == 0


@pytest.mark.django_db
def test_confirm_order_cancellation(cancellation_event: Event):
    event = cancellation_event
    order_id = _make_order(event, datetime.now(UTC), {}, status=PaymentStatus.PAID)

    RequestOrderCancellation.mutate(None, None, _request_input(event, order_id))
    token = OrderCancellationToken.objects.get(event=event, order_id=order_id, state="valid")

    # wrong code is rejected
    with pytest.raises(OrderCancellationToken.DoesNotExist):
        ConfirmOrderCancellation.mutate(None, None, _confirm_input(event, order_id, "bogus"))

    ConfirmOrderCancellation.mutate(None, None, _confirm_input(event, order_id, token.code))

    token.refresh_from_db()
    assert token.state == "used"
    assert _get_order(event, order_id).status == PaymentStatus.CANCELLED

    # the token cannot be used again
    with pytest.raises(OrderCancellationToken.DoesNotExist):
        ConfirmOrderCancellation.mutate(None, None, _confirm_input(event, order_id, token.code))


@pytest.mark.django_db
def test_confirm_order_cancellation_no_longer_eligible(cancellation_event: Event):
    """
    Eligibility is re-checked at confirmation time. If the order is no longer
    eligible (eg. the cancellation period was changed or the event has started),
    the token is rejected and remains valid (so that nothing happened is clear).
    """
    event = cancellation_event
    order_id = _make_order(event, datetime.now(UTC), {}, status=PaymentStatus.PAID)

    RequestOrderCancellation.mutate(None, None, _request_input(event, order_id))
    token = OrderCancellationToken.objects.get(event=event, order_id=order_id, state="valid")

    meta = TicketsV2EventMeta.objects.get(event=event)
    meta.cancellation_period_days = 0
    meta.save(update_fields=["cancellation_period_days"])

    with pytest.raises(ValueError):
        ConfirmOrderCancellation.mutate(None, None, _confirm_input(event, order_id, token.code))

    token.refresh_from_db()
    assert token.state == "valid"
    assert _get_order(event, order_id).status == PaymentStatus.PAID


@pytest.mark.django_db
def test_receipt_cancellation_link(cancellation_event: Event):
    event = cancellation_event
    product = Product.objects.create(
        event=event,
        title="Test ticket",
        description="",
        price=Decimal("10.00"),
        vat_percentage=Decimal("25.50"),
    )
    order_id = _make_order(
        event,
        datetime.now(UTC),
        {product.id: 1},
        status=PaymentStatus.PENDING,
        total_price=Decimal("10.00"),
    )
    _add_provider_paid_stamp(event, order_id)
    order = _get_order(event, order_id)

    PendingReceipt.event_cache_refreshed_at = None
    receipt = PendingReceipt.from_order(order)
    assert receipt.is_customer_cancellable
    assert f"/orders/{order_id}/cancel" in receipt.body

    # when self-service cancellation is disabled, the receipt has no cancellation link
    meta = TicketsV2EventMeta.objects.get(event=event)
    meta.cancellation_period_days = 0
    meta.save(update_fields=["cancellation_period_days"])

    PendingReceipt.event_cache_refreshed_at = None
    receipt = PendingReceipt.from_order(order)
    assert not receipt.is_customer_cancellable
    assert "/cancel" not in receipt.body


@pytest.mark.django_db
def test_confirm_order_cancellation_expired_token(cancellation_event: Event):
    """
    A confirmation link can only be used for a limited time after it was
    requested, even if the order remains cancellable. A new link can always
    be requested.
    """
    event = cancellation_event
    order_id = _make_order(event, datetime.now(UTC), {}, status=PaymentStatus.PAID)

    RequestOrderCancellation.mutate(None, None, _request_input(event, order_id))
    token = OrderCancellationToken.objects.get(event=event, order_id=order_id, state="valid")
    OrderCancellationToken.objects.filter(pk=token.pk).update(created_at=datetime.now(UTC) - timedelta(hours=25))

    with pytest.raises(ValueError):
        ConfirmOrderCancellation.mutate(None, None, _confirm_input(event, order_id, token.code))

    assert _get_order(event, order_id).status == PaymentStatus.PAID


# The optimized server's event cache is an async-lru (alru_cache) wrapped loader.
# These tests stub the DB loader (_do_load) and drive the cache through Event.get(),
# so they exercise alru_cache's real TTL/single-flight machinery. alru_cache binds to
# the running event loop, so asyncio.run()'s throwaway loop triggers a (harmless)
# AlruCacheLoopResetWarning we silence here.
_ALRU_LOOP_RESET_WARNING = "ignore:alru_cache detected event loop change"


@pytest.mark.filterwarnings(_ALRU_LOOP_RESET_WARNING)
def test_optimized_server_event_cache_single_flight():
    """
    The optimized server serves hundreds of requests concurrently on a single event
    loop. When the event cache is cold or its TTL has expired, only one request should
    load it from the database; the rest must coalesce onto that single load rather than
    each kicking off its own (a cache stampede).
    """
    import asyncio
    from unittest.mock import patch

    from kompassi.tickets_v2.optimized_server.models.event import Event as OptimizedEvent

    async def scenario():
        load_calls = 0

        async def fake_load():
            nonlocal load_calls
            load_calls += 1
            # Yield control to let every other queued request pile up while this one
            # is "hitting the database"; without single-flight they would each load too.
            await asyncio.sleep(0.05)
            return {"tracon": object()}

        OptimizedEvent._load_all.cache_clear()  # type: ignore[attr-defined]  # alru_cache wrapper
        with patch.object(OptimizedEvent, "_do_load", staticmethod(fake_load)):
            results = await asyncio.gather(*(OptimizedEvent.get("tracon") for _ in range(200)))

        return load_calls, results

    load_calls, results = asyncio.run(scenario())

    assert load_calls == 1
    assert all(result is not None for result in results)


@pytest.mark.filterwarnings(_ALRU_LOOP_RESET_WARNING)
def test_optimized_server_event_cache_refresh_survives_waiter_cancellation():
    """
    A request that gives up while waiting for an in-flight cache load (e.g. the client
    disconnected, cancelling the asyncio task) must not abort that load for the requests
    still waiting on it, nor cause a duplicate load. An earlier hand-rolled shared-Future
    approach broke here: cancelling any waiter cancelled the single shared task, failing
    every other in-flight request. This guards that alru_cache does not regress that.
    """
    import asyncio
    from unittest.mock import patch

    from kompassi.tickets_v2.optimized_server.models.event import Event as OptimizedEvent

    async def scenario():
        load_calls = 0

        async def fake_load():
            nonlocal load_calls
            load_calls += 1
            await asyncio.sleep(0.05)
            return {"tracon": object()}

        OptimizedEvent._load_all.cache_clear()  # type: ignore[attr-defined]  # alru_cache wrapper
        with patch.object(OptimizedEvent, "_do_load", staticmethod(fake_load)):
            tasks = [asyncio.ensure_future(OptimizedEvent.get("tracon")) for _ in range(50)]
            # Let the first task start the load while the rest coalesce behind it.
            await asyncio.sleep(0.01)
            # The latter half of the waiters "disconnect" and give up mid-load.
            for task in tasks[25:]:
                task.cancel()
            results = await asyncio.gather(*tasks, return_exceptions=True)

        return load_calls, results

    load_calls, results = asyncio.run(scenario())

    # Exactly one load, despite half the waiters bailing out.
    assert load_calls == 1
    # The waiters that did not cancel still got a valid result.
    survivors = results[:25]
    assert all(not isinstance(result, BaseException) and result is not None for result in survivors)


@pytest.mark.django_db
def test_confirm_order_cancellation_creates_cancellation_receipt(cancellation_event: Event):
    """
    Confirming a customer cancellation must leave a final "order cancelled" receipt
    in the Receipt table, which the receipt worker emails to the customer and the
    admin UI shows. (The confirmation-request email is sent directly and is
    deliberately not a receipt.)
    """
    from kompassi.tickets_v2.models.receipt import Receipt
    from kompassi.tickets_v2.optimized_server.models.enums import ReceiptType

    event = cancellation_event
    # A free (zero-price) order: paid via a NONE-provider stamp, refunded via NONE.
    order_id = _make_order(event, datetime.now(UTC), {}, status=PaymentStatus.NOT_STARTED)
    PaymentStamp(
        event=event,
        order_id=order_id,
        correlation_id=uuid7(),
        provider_id=PaymentProvider.NONE,
        type=PaymentStampType.PAYMENT_CALLBACK,
        status=PaymentStatus.PAID,
        data={},
    ).save()

    RequestOrderCancellation.mutate(None, None, _request_input(event, order_id))
    token = OrderCancellationToken.objects.get(event=event, order_id=order_id, state="valid")
    ConfirmOrderCancellation.mutate(None, None, _confirm_input(event, order_id, token.code))

    assert _get_order(event, order_id).status == PaymentStatus.CANCELLED

    cancellation_receipts = Receipt.objects.filter(
        event=event,
        order_id=order_id,
        type=ReceiptType.CANCELLED,
    )
    assert cancellation_receipts.count() == 1


@pytest.mark.django_db
def test_auto_cancelled_unpaid_order_creates_no_receipt(cancellation_event: Event):
    """
    The cron that auto-cancels abandoned *unpaid* orders must not create a receipt
    (and thus must not email the customer). Only orders that were actually paid get
    a cancellation receipt. Guards the intent of migration 0007.
    """
    from kompassi.tickets_v2.models.enums import ActorType
    from kompassi.tickets_v2.models.receipt import Receipt
    from kompassi.tickets_v2.optimized_server.models.enums import RefundType

    event = cancellation_event
    order_id = _make_order(event, datetime.now(UTC), {}, status=PaymentStatus.NOT_STARTED)

    _get_order(event, order_id).cancel_and_refund(RefundType.NONE, actor_type=ActorType.SYSTEM)

    assert _get_order(event, order_id).status == PaymentStatus.CANCELLED
    assert not Receipt.objects.filter(event=event, order_id=order_id).exists()


@pytest.mark.django_db
def test_provider_refund_creates_single_refunded_receipt(cancellation_event: Event):
    """
    A provider refund records CREATE_REFUND_SUCCESS synchronously (status
    REFUND_REQUESTED) and a REFUNDED stamp later via Paytrail's async refund
    callback, both sharing one correlation_id. The customer must get exactly one
    REFUNDED receipt, created as soon as the refund is accepted rather than being
    deferred to the callback (which never arrives in dev).
    """
    from kompassi.tickets_v2.models.receipt import Receipt
    from kompassi.tickets_v2.optimized_server.models.enums import ReceiptType

    event = cancellation_event
    order_id = _make_order(
        event,
        datetime.now(UTC),
        {},
        status=PaymentStatus.NOT_STARTED,
        total_price=Decimal("10.00"),
    )
    _add_provider_paid_stamp(event, order_id)
    refund_correlation = uuid7()

    # Provider accepted the refund (recorded synchronously at confirmation time).
    PaymentStamp(
        event=event,
        order_id=order_id,
        correlation_id=refund_correlation,
        provider_id=PaymentProvider.PAYTRAIL,
        type=PaymentStampType.CREATE_REFUND_SUCCESS,
        status=PaymentStatus.REFUND_REQUESTED,
        data={},
    ).save()

    refunded_receipts = Receipt.objects.filter(event=event, order_id=order_id, type=ReceiptType.REFUNDED)
    assert refunded_receipts.count() == 1

    # The async refund callback (same correlation_id) must not create a second receipt.
    PaymentStamp(
        event=event,
        order_id=order_id,
        correlation_id=refund_correlation,
        provider_id=PaymentProvider.PAYTRAIL,
        type=PaymentStampType.REFUND_CALLBACK,
        status=PaymentStatus.REFUNDED,
        data={},
    ).save()

    assert refunded_receipts.count() == 1


@pytest.mark.django_db
def test_order_cancellation_token_cleanup(cancellation_event: Event):
    """
    Expired cancellation tokens are swept by the scheduled cleanup. Filtering on
    created_at (not used_at) means even never-clicked valid tokens are removed once
    they are long past their 24h validity; recent tokens are kept.
    """
    from kompassi.core.utils.cleanup import perform_cleanup

    event = cancellation_event
    order_id = _make_order(event, datetime.now(UTC), {}, status=PaymentStatus.PAID)

    recent = OrderCancellationToken.objects.create(event=event, order_id=order_id, language="en")
    old = OrderCancellationToken.objects.create(event=event, order_id=order_id, language="en")
    # auto_now_add prevents setting created_at on create, so backdate it afterwards.
    OrderCancellationToken.objects.filter(pk=old.pk).update(created_at=datetime.now(UTC) - timedelta(days=31))

    perform_cleanup()

    assert OrderCancellationToken.objects.filter(pk=recent.pk).exists()
    assert not OrderCancellationToken.objects.filter(pk=old.pk).exists()
