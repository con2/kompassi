import logging

from csp.decorators import csp_update
from django.contrib import messages
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from kompassi.core.helpers import person_required

from ..models import Privilege

logger = logging.getLogger(__name__)

# FMH slack is chaining redirects and all redirects in the chain need to be allowed
SLACK_INVITE_ORIGINS = [
    "https://con2.slack.com",
    "https://desucon.slack.com",
    "https://join.slack.com",
    "https://slack.com",
    "https://traconfi.slack.com",
]


@person_required
@csp_update({"form-action": SLACK_INVITE_ORIGINS})  # type: ignore
def access_profile_privileges_view(request):
    person = request.user.person

    vars = dict(
        granted_privileges=person.granted_privileges.all(),
        potential_privileges=Privilege.get_potential_privileges(person),
    )

    return render(request, "access_profile_privileges_view.pug", vars)


@person_required
def access_profile_privilege_view(request, privilege_slug):
    person = request.user.person
    privilege = get_object_or_404(Privilege, slug=privilege_slug)

    granted_privilege = person.granted_privileges.filter(privilege=privilege).first()
    potential_privilege = Privilege.get_potential_privileges(person, id=privilege.id).first()

    if not granted_privilege and not potential_privilege:
        messages.error(
            request,
            (
                "Et voi tällä hetkellä hankkia tätä käyttöoikeutta itsepalveluna. "
                "Mikäli epäilet tässä olevan virheen, ota yhteys käyttöoikeudesta vastaavan tapahtuman järjestäjiin."
            ),
        )
        return redirect("access_profile_privileges_view")

    vars = dict(
        granted_privilege=granted_privilege,
        privilege=potential_privilege,
    )

    return render(request, "access_profile_privilege_view.pug", vars)


@person_required
@require_POST
@csp_update({"form-action": SLACK_INVITE_ORIGINS})  # type: ignore
def access_profile_request_privilege_view(request, privilege_slug):
    if not request.user.person.is_email_verified:
        messages.error(request, "Käyttöoikeuden pyytäminen edellyttää vahvistettua sähköpostiosoitetta.")
        return redirect("access_profile_privileges_view")

    # People belonging to both Hitpoint and Tracon concoms were getting MultipleObjectsReturned here.
    # Cannot use get_object_or_404 due to the same object being returned multiple times via multiple groups.
    # get_object_or_404 uses .get which has no way to provide .distinct() from outside.
    privilege = Privilege.objects.filter(
        slug=privilege_slug,
        group_privileges__group__in=request.user.groups.all(),
    ).first()
    if privilege is None:
        raise Http404("Privilege not found")

    privilege.grant(request.user.person)

    if privilege.request_success_message:
        success_message = privilege.request_success_message
    else:
        success_message = "Käyttöoikeuden pyytäminen onnistui."

    messages.success(request, success_message)

    if privilege.slack_access:
        return redirect(privilege.slack_access.invite_link)
    else:
        return redirect("access_profile_privileges_view")
