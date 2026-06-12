import json
from datetime import UTC, datetime
from decimal import Decimal
from functools import cached_property
from typing import Any, Literal
from uuid import UUID, uuid4

import pydantic
import pytest
import requests

from kompassi.core.models.event import Event
from kompassi.tickets_v2.models.order import Order
from kompassi.tickets_v2.models.product import Product
from kompassi.tickets_v2.optimized_server.models.api import CreateOrderResponse, GetOrderResponse, GetProductsResponse
from kompassi.tickets_v2.optimized_server.models.customer import Customer
from kompassi.tickets_v2.optimized_server.models.enums import PaymentStatus
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
                "0",
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
