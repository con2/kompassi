# encoding: utf-8

from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from core.helpers import person_required

from .models import Privilege


@person_required
def access_profile_privileges_view(request):
    person = request.user.person

    vars = dict(
        granted_privileges=person.granted_privileges.all(),
        potential_privileges=Privilege.get_potential_privileges(person),
    )

    return render(request, 'access_profile_privileges_view.jade', vars)


@person_required
@require_POST
def access_profile_request_privilege_view(request, privilege_slug):
    if not request.user.person.is_email_verified:
        messages.error(request, u'Käyttöoikeuden pyytäminen edellyttää vahvistettua sähköpostiosoitetta.')
        return redirect('access_profile_privileges_view')

    # People belonging to both Hitpoint and Tracon concoms were getting MultipleObjectsReturned here.
    # Cannot use get_object_or_404 due to the same object being returned multiple times via multiple groups.
    # get_object_or_404 uses .get which has no way to provide .distinct() from outside.
    privilege = Privilege.objects.filter(
        slug=privilege_slug,
        group_privileges__group__in=request.user.groups.all(),
    ).first()
    if privilege is None:
        raise Http404('Privilege not found')

    privilege.grant(request.user.person)

    if privilege.request_success_message:
        success_message = privilege.request_success_message
    else:
        success_message = u'Käyttöoikeuden pyytäminen onnistui.'

    messages.success(request, success_message)
    return redirect('access_profile_privileges_view')


def access_profile_menu_items(request):
    privileges_url = reverse('access_profile_privileges_view')
    privileges_active = request.path.startswith(privileges_url)
    privileges_text = u"Käyttöoikeudet"

    return [
        (privileges_active, privileges_url, privileges_text),
    ]
