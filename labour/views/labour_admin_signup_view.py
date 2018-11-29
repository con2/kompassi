# encoding: utf-8



from collections import Counter, OrderedDict, namedtuple
import json

import datetime

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db.models import Q, Sum
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_http_methods, require_safe
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from dateutil.tz import tzlocal

from core.csv_export import csv_response, CSV_EXPORT_FORMATS, EXPORT_FORMATS
from core.sort_and_filter import Filter, Sorter
from core.models import Event, Person
from core.tabs import Tab
from core.utils import initialize_form, url

from ..forms import AdminPersonForm, SignupForm, SignupAdminForm
from ..helpers import labour_admin_required, labour_event_required
from ..models.constants import SIGNUP_STATE_NAMES
from ..models import (
    JobCategory,
    LabourEventMeta,
    PersonQualification,
    Qualification,
    Signup,
)
from ..proxies.signup.onboarding import SignupOnboardingProxy

from .view_helpers import initialize_signup_forms


@labour_admin_required
@require_http_methods(['GET', 'HEAD', 'POST'])
def labour_admin_signup_view(request, vars, event, person_id):
    person = get_object_or_404(Person, pk=int(person_id))
    signup = get_object_or_404(Signup, person=person, event=event)

    old_state_flags = signup._state_flags

    signup_form, signup_extra_form, signup_admin_form = initialize_signup_forms(
        request, event, signup,
        admin=True
    )
    person_form = initialize_form(AdminPersonForm, request,
        instance=signup.person,
        prefix='person',
        readonly=True,
        event=event,
    )

    if request.method == 'POST':
        # XXX Need to update state before validation to catch accepting people without accepted job categories
        for state_name in signup.next_states:
            command_name = 'set-state-{state_name}'.format(state_name=state_name)
            if command_name in request.POST:
                old_state_flags = signup._state_flags
                signup.state = state_name
                break

        if signup_form.is_valid() and signup_extra_form.is_valid() and signup_admin_form.is_valid():
            signup_form.save()
            signup_extra_form.save()
            signup_admin_form.save()

            signup.apply_state()
            messages.success(request, 'Tiedot tallennettiin.')

            if 'save-return' in request.POST:
                return redirect('labour_admin_signups_view', event.slug)
            else:
                return redirect('labour_admin_signup_view', event.slug, person.pk)
        else:
            # XXX Restore state just for shows, suboptimal but
            signup._state_flags = old_state_flags

            messages.error(request, 'Ole hyvä ja tarkista lomake.')

    non_qualified_category_names = [
        jc.name for jc in JobCategory.objects.filter(event=event)
        if not jc.is_person_qualified(signup.person)
    ]

    non_applied_categories = list(JobCategory.objects.filter(event=event))
    for applied_category in signup.job_categories.all():
        non_applied_categories.remove(applied_category)
    non_applied_category_names = [cat.name for cat in non_applied_categories]

    previous_signup, next_signup = signup.get_previous_and_next_signup()

    historic_signups = Signup.objects.filter(person=signup.person).exclude(event=event).order_by('-event__start_time')
    if not person.allow_work_history_sharing:
        # The user has elected to not share their full work history between organizations.
        # Only show work history for the current organization.
        historic_signups = historic_signups.filter(event__organization=event.organization)

    tabs = [
        Tab('labour-admin-signup-state-tab', 'Hakemuksen tila', active=True),
        Tab('labour-admin-signup-person-tab', 'Hakijan tiedot'),
        Tab('labour-admin-signup-application-tab', 'Hakemuksen tiedot'),
        Tab('labour-admin-signup-messages-tab', 'Työvoimaviestit', notifications=signup.person_messages.count()),
        Tab('labour-admin-signup-shifts-tab', 'Työvuorot'),
        Tab('labour-admin-signup-history-tab', 'Työskentelyhistoria', notifications=historic_signups.count()),
    ]

    vars.update(
        historic_signups=historic_signups,
        next_signup=next_signup,
        person_form=person_form,
        previous_signup=previous_signup,
        signup=signup,
        signup_admin_form=signup_admin_form,
        signup_extra_form=signup_extra_form,
        signup_form=signup_form,
        tabs=tabs,
        total_hours=signup.shifts.all().aggregate(Sum('hours'))['hours__sum'],

        # XXX hack: widget customization is very difficult, so apply styles via JS
        non_applied_category_names_json=json.dumps(non_applied_category_names),
        non_qualified_category_names_json=json.dumps(non_qualified_category_names),
    )

    person.log_view(request, event=event)

    return render(request, 'labour_admin_signup_view.pug', vars)
