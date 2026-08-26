from datetime import timedelta

from django.contrib.auth.models import AbstractBaseUser
from django.http import HttpRequest
from django.utils.timezone import now

from kompassi.event_log_v2.utils.emit import emit

from .constants import CBAC_SUDO_CLAIMS, CBAC_SUDO_VALID_MINUTES
from .exceptions import CBACPermissionDenied
from .models.cbac_entry import CBACEntry, Claims


def grant_sudo(user: AbstractBaseUser, claims: Claims, request: HttpRequest | None = None) -> CBACEntry:
    """
    Mints a temporary CBAC entry for a superuser overriding a permission denial.
    Shared by V1's sudo_view and V2's sudoCbac mutation so there is one implementation
    and one audit trail.
    """
    if not user.is_superuser:  # type: ignore[union-attr]
        raise CBACPermissionDenied(claims)

    claims = {k: v for (k, v) in claims.items() if k in CBAC_SUDO_CLAIMS}
    if not claims:
        # CBACEntry.is_allowed uses claims__contained_by, under which a {} claims
        # entry matches everything. Sudo must never mint one.
        raise ValueError("sudo cannot grant an unrestricted permission")

    cbac_entry = CBACEntry(
        user=user,
        valid_until=now() + timedelta(minutes=CBAC_SUDO_VALID_MINUTES),
        claims=claims,
        created_by=user,
    )
    cbac_entry.save()

    emit("access.cbac.sudo", request=request, other_fields=cbac_entry.as_dict())
    emit("access.cbacentry.created", request=request, other_fields=cbac_entry.as_dict())

    return cbac_entry
