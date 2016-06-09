# encoding: utf-8

from __future__ import unicode_literals

from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from labour.proxies.signup.onboarding import SignupOnboardingProxy

from ..helpers import badges_admin_required
from ..models import Badge


@badges_admin_required
@require_http_methods(['GET', 'HEAD', 'POST'])
def badges_admin_onboarding_view(request, vars, event):
    if request.method in ('GET', 'HEAD'):
        badges = Badge.objects.filter(
            personnel_class__event=event,
            revoked_at__isnull=True,
        ).order_by('surname', 'first_name')

        vars.update(
            badges=badges,
        )

        return render(request, 'badges_admin_onboarding_view.jade', vars)
    elif request.method == 'POST':
        badge_id = request.POST['id']
        is_arrived = request.POST['arrived'] == 'true'

        badge = get_object_or_404(Badge, id=int(badge_id))
        badge.is_arrived = is_arrived
        badge.save()

        if badge.person:
            sop = SignupOnboardingProxy.objects.filter(event=event, person=badge.person, is_active=True).first()
            if sop:
                sop.mark_arrived(is_arrived)

        return HttpResponse()
    else:
        raise NotImplementedError(request.method)
