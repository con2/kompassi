from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_safe

from kompassi.core.models import Person

from .utils import api_login_required, api_view


@require_safe
@api_view
@api_login_required
def api_person_view(request, username):
    user = get_object_or_404(User, username=username)
    person = get_object_or_404(Person, user=user)

    return person.as_dict()


@require_safe
@api_view
def api_status_view(request):
    return dict(status="OK")
