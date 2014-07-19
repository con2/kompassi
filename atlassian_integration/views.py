# encoding: utf-8

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views.decorators.http import require_GET

from core.utils import get_next

from .utils import crowd_login, CrowdError


@login_required
@require_GET
def crowd_session_view(request):
    next = get_next(request)

    try:
        crowd_cookie = crowd_login(username=request.user.username, request=request)
    except CrowdError, e:
        messages.error(request,
            u'Kirjautuminen Atlassian-tuotteiden kertakirjautumispalveluun epäonnistui. '
            u'Voit käyttää useimpia {kompassin} palveluita normaalisti, mutta jotkin toiminnot, '
            u'kuten työvoimawiki, eivät välttämättä toimi. Jos ongelma toistuu, ole hyvä ja ota '
            u'yhteyttä: {adminiin}'
            .format(
                kompassin=settings.KOMPASSI_INSTALLATION_NAME_GENITIVE,
                adminiin=settings.DEFAULT_FROM_EMAIL,
            )
        )

        # Unsafe to redirect back to Confluence, would cause infinite redirection loop.
        # So disregard "next" and redirect back to front page.
        return redirect('core_frontpage_view')

    response = redirect(next)
    response.set_cookie(**crowd_cookie)

    return response    