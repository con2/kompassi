import json
from functools import cached_property
from typing import Any, Literal
from uuid import UUID, uuid4

import pydantic
import pytest
import requests

from kompassi.core.models.event import Event
from kompassi.tickets_v2.optimized_server.models.api import CreateOrderResponse, GetOrderResponse, GetProductsResponse
from kompassi.tickets_v2.optimized_server.models.customer import Customer
from kompassi.tickets_v2.optimized_server.models.enums import PaymentStatus
from kompassi.tickets_v2.optimized_server.models.order import CreateOrderRequest
from kompassi.tickets_v2.optimized_server.providers.paytrail import PaymentCallback, PaytrailStatus
from kompassi.tickets_v2.optimized_server.utils.paytrail_hmac import calculate_hmac
from kompassi.tickets_v2.optimized_server.utils.uuid7 import uuid7

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
