import logging

from django.shortcuts import render

from ..constants import CBAC_SUDO_CLAIMS
from ..exceptions import CBACPermissionDenied

logger = logging.getLogger("kompassi")


def permission_denied_view(request, exception=None):
    sudo_claims = {}

    if request.user.is_superuser and isinstance(exception, CBACPermissionDenied):
        sudo_claims = {k: v for (k, v) in exception.claims.items() if k in CBAC_SUDO_CLAIMS}

    vars = dict(
        sudo_claims=sudo_claims,
        next=request.path,
    )

    return render(request, "403.pug", vars)


def not_found_view(request, exception=None):
    return render(
        request,
        "404.pug",
        {
            "event": None,
            "login_page": True,
        },
    )
