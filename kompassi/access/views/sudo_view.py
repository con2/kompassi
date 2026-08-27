import logging

from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect

from ..constants import CBAC_SUDO_CLAIMS, CBAC_SUDO_VALID_MINUTES
from ..sudo import grant_sudo

logger = logging.getLogger(__name__)


@user_passes_test(lambda u: u.is_superuser)  # type: ignore
def sudo_view(request):
    next = request.GET.get("next") or "/"
    claims = {k: v for (k, v) in request.POST.items() if k in CBAC_SUDO_CLAIMS}

    grant_sudo(request.user, claims, request=request)

    messages.warning(
        request,
        f"Käyttöoikeustarkastus ohitettu pääkäyttäjän oikeuksin. "
        f"Väliaikainen käyttöoikeus on voimassa {CBAC_SUDO_VALID_MINUTES} minuuttia.",
    )

    return redirect(next)
