# encoding: utf-8

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_http_methods

from core.helpers import initialize_form, url
from core.models import Event

from ..forms import SignupForm
from ..helpers import labour_admin_required
from ..models import LabourEventMeta, Qualification, PersonQualification, Signup


@labour_admin_required
def labour_admin_dashboard_view(request, vars, event):
    vars.update(
        signups=event.signup_set.order_by('-created_at')[:5]
    )

    return render(request, 'labour_admin_dashboard_view.jade', vars)


@labour_admin_required
def labour_admin_signup_view(request, vars, event, person):
    signup = get_object_or_404(Signup, person=int(person), event=event)

    vars.update(
        signup=signup,
    )

    return render(request, 'labour_admin_signup_view.jade', vars)


@labour_admin_required
def labour_admin_signups_view(request, vars, event):
    signups = event.signup_set.all()

    vars.update(
        signups=signups,
    )

    return render(request, 'labour_admin_signups_view.jade', vars)


def labour_admin_menu_items(request, event):
    dashboard_url = url('labour_admin_dashboard_view', event.slug)
    dashboard_active = request.path == dashboard_url
    dashboard_text = u"Kojelauta"

    signups_url = url('labour_admin_signups_view', event.slug)
    signups_active = request.path.startswith(signups_url)
    signups_text = u"Tapahtumaan ilmoittautuneet henkilöt"

    return [
        (dashboard_active, dashboard_url, dashboard_text),
        (signups_active, signups_url, signups_text),
    ]
