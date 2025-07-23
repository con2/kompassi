import logging
from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect
from django.utils.timezone import now

from kompassi.event_log_v2.utils.emit import emit

from ..constants import CBAC_SUDO_CLAIMS, CBAC_SUDO_VALID_MINUTES
from ..models import CBACEntry

logger = logging.getLogger(__name__)


@user_passes_test(lambda u: u.is_superuser)  # type: ignore
def sudo_view(request):
    next = request.GET.get("next") or "/"
    claims = {k: v for (k, v) in request.POST.items() if k in CBAC_SUDO_CLAIMS}

    cbac_entry = CBACEntry(
        user=request.user,
        valid_until=now() + timedelta(minutes=CBAC_SUDO_VALID_MINUTES),
        claims=claims,
        created_by=request.user,
    )
    cbac_entry.save()

    messages.warning(
        request,
        f"Käyttöoikeustarkastus ohitettu pääkäyttäjän oikeuksin. "
        f"Väliaikainen käyttöoikeus on voimassa {CBAC_SUDO_VALID_MINUTES} minuuttia.",
    )

    emit("access.cbac.sudo", request=request, other_fields=cbac_entry.as_dict())
    emit("access.cbacentry.created", request=request, other_fields=cbac_entry.as_dict())

    return redirect(next)
