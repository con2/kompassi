from django.views.decorators.http import require_GET
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from core.models import Person

from .utils import api_view, api_login_required, pick_attrs


@require_GET
@api_view
@api_login_required
def api_person_view(request, username):
    user = get_object_or_404(User, username=username)
    person = get_object_or_404(Person, user=user)

    return dict(
        pick_attrs(person,
            'first_name',
            'surname',
            'nick',
            'full_name',
            'display_name',

            'phone',
            'email',
            'birth_date',
        ),

        username=user.username,
        groups=[group.name for group in user.groups.all()],
    )
