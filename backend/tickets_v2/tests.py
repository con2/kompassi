import json

from tickets_v2.optimized_server.utils.paytrail_hmac import calculate_hmac


def test_paytrail_hmac():
    account = "375917"
    secret = "SAIPPUAKAUPPIAS"

    headers = {
        "checkout-account": account,
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

    assert calculate_hmac(secret, headers, body) == "3708f6497ae7cc55a2e6009fc90aa10c3ad0ef125260ee91b19168750f6d74f6"
