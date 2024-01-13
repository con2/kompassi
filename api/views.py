from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_safe

from core.models import Person
from labour.helpers import labour_event_required

from .utils import api_login_required, api_view, cbac_api_view


@require_safe
@api_view
@api_login_required
def api_person_view(request, username):
    user = get_object_or_404(User, username=username)
    person = get_object_or_404(Person, user=user)

    return person.as_dict()


@require_safe
@cbac_api_view
@labour_event_required
def api_discord_view(request, event):
    """
    Supplies discord handles for role bot integration.
    """
    SignupExtra = event.labour_event_meta.signup_extra_model
    return [
        extra.as_dict(format="discord")
        # is_active is implied by is_alive but it is also denormalized into the db so use it to optimize
        for extra in SignupExtra.objects.filter(is_active=True).select_related("person")
        if extra.person.discord_handle and extra.discord_roles
    ]


@require_safe
@api_view
def api_status_view(request):
    return dict(status="OK")
