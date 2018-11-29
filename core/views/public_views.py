# encoding: utf-8

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.timezone import now
from django.views.decorators.http import require_http_methods, require_safe

from ..models import (
    EmailVerificationError,
    EmailVerificationToken,
    Event,
    Organization,
    PasswordResetError,
    PasswordResetToken,
    Person,
)
from ..forms import (
    LoginForm,
    PasswordForm,
    PasswordResetForm,
    PasswordResetRequestForm,
    PersonForm,
    RegistrationForm,
)
from ..utils import (
    get_next,
    groups_of_n,
    initialize_form,
    url,
)
from ..helpers import person_required, public_organization_required


@public_organization_required
def core_organization_view(request, organization):
    t = now()

    past_events = Event.objects.filter(organization=organization, public=True, end_time__lte=t).order_by('-start_time')
    current_events = Event.objects.filter(organization=organization, public=True, start_time__lte=t, end_time__gt=t).order_by('-start_time')
    future_events = Event.objects.filter(Q(organization=organization, public=True) & (Q(start_time__gt=t) | Q(start_time__isnull=True))).order_by('start_time')

    vars = dict(
        organization=organization,
        past_events_rows=list(groups_of_n(past_events, 4)),
        current_events_rows=list(groups_of_n(current_events, 4)),
        future_events_rows=list(groups_of_n(future_events, 4)),
    )

    if 'membership' in settings.INSTALLED_APPS:
        from membership.views import membership_organization_box_context
        vars.update(membership_organization_box_context(request, organization))

    return render(request, 'core_organization_view.pug', vars)

def core_event_view(request, event_slug):
    event = get_object_or_404(Event, slug=event_slug)

    vars = dict(
        event=event,
        settings=settings,
    )

    if event.enrollment_event_meta:
        from enrollment.views import enrollment_event_box_context
        vars.update(enrollment_event_box_context(request, event))

    if event.labour_event_meta:
        from labour.views import labour_event_box_context
        vars.update(labour_event_box_context(request, event))

    if event.programme_event_meta:
        from programme.views import programme_event_box_context
        vars.update(programme_event_box_context(request, event))

    if event.tickets_event_meta:
        from tickets.views import tickets_event_box_context
        vars.update(tickets_event_box_context(request, event))

    if event.badges_event_meta:
        from badges.views import badges_event_box_context
        vars.update(badges_event_box_context(request, event))

    # if event.sms_event_meta:
    #     from sms.views import sms_event_box_context
    #     vars.update(sms_event_box_context(request, event))

    if event.intra_event_meta:
        from intra.views import intra_event_box_context
        vars.update(intra_event_box_context(request, event))

    return render(request, 'core_event_view.pug', vars)
