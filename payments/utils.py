import hmac
from typing import Dict

import requests


def calculate_hmac(
    secret: str,
    params: dict[str, str],
    body: str = None,
    encoding="UTF-8",
    hash_algorithm="sha256",
):
    """
    :param secret: Merchant shared secret
    :param params: Headers or query string parameters
    :param body: Request body or empty string for GET requests

    Based on the following Node.js example code from
    https://checkoutfinland.github.io/psp-api/#/examples?id=hmac-calculation-node-js

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
    for key in sorted(params.keys()):
        if key.startswith("checkout-"):
            hmac_payload_parts.append(f"{key}:{params[key]}")
    hmac_payload_parts.append(body if body else "")
    hmac_payload = "\n".join(hmac_payload_parts)
    return hmac.new(
        key=secret.encode(encoding),
        msg=hmac_payload.encode(encoding),
        digestmod=hash_algorithm,
    ).hexdigest()
