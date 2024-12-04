import hmac
from collections.abc import Mapping


def calculate_hmac(
    secret: str,
    params: Mapping[str, str],
    body: str | None = None,
    encoding="UTF-8",
    hash_algorithm="sha256",
):
    """
    Calculate the HMAC-SHA256/SHA512 digest as specified by Paytrail's API documentation.

    :param secret: Merchant shared secret
    :param params: Headers or query string parameters
    :param body: Request body or empty string for GET requests

    Based on the following Node.js example code from
    https://docs.paytrail.com/#/examples?id=hmac-calculation-nodejs

    ```javascript
    const calculateHmac = (secret, params, body) => {
        const hmacPayload =
            Object.keys(params)
            .sort()
            .map((key) => [ key, params[key] ].join(':'))
            .concat(body ? JSON.stringify(body) : '')
            .join("\n");

        return crypto
            .createHmac('sha256', secret)
            .update(hmacPayload)
            .digest('hex');
    ```
    };
    """
    hmac_payload_parts = []
    for key, value in sorted(params.items()):
        if key.startswith("checkout-"):
            hmac_payload_parts.append(f"{key}:{value}")
    hmac_payload_parts.append(body if body else "")
    hmac_payload = "\n".join(hmac_payload_parts)
    return hmac.new(
        key=secret.encode(encoding),
        msg=hmac_payload.encode(encoding),
        digestmod=hash_algorithm,
    ).hexdigest()
