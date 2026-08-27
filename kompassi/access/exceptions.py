from typing import Any

from django.core.exceptions import PermissionDenied

from .constants import CBAC_PERMISSION_DENIED, CBAC_SUDO_CLAIMS
from .models.cbac_entry import Claims


class CBACPermissionDenied(PermissionDenied):
    def __init__(self, claims: Claims, expose_claims: bool = False):
        super().__init__("Permission denied")
        self.claims = claims
        self.extensions: dict[str, Any] = {"code": CBAC_PERMISSION_DENIED}
        if expose_claims:
            self.extensions["claims"] = {k: v for (k, v) in claims.items() if k in CBAC_SUDO_CLAIMS}
