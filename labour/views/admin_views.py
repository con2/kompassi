# encoding: utf-8

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_http_methods

from core.forms import PersonForm
from core.models import Event, Person
from core.utils import initialize_form, url, json_response, render_string

from ..forms import SignupForm
from ..helpers import labour_admin_required
from ..models import LabourEventMeta, Qualification, PersonQualification, Signup, JobCategory

from .view_helpers import initialize_signup_forms


@labour_admin_required
def labour_admin_dashboard_view(request, vars, event):
    vars.update(
        signups=event.signup_set.order_by('-created_at')[:5]
    )

    return render(request, 'labour_admin_dashboard_view.jade', vars)


@labour_admin_required
def labour_admin_signup_view(request, vars, event, person_id):
    person = get_object_or_404(Person, pk=person_id)
    signup = get_object_or_404(Signup, person=person, event=event)

    signup_form, signup_extra_form = initialize_signup_forms(request, event, signup,
        readonly=True
    )
    person_form = initialize_form(PersonForm, request,
        instance=signup.person,
        prefix='person',
        submit_button=False,
        readonly=True
    )

    vars.update(
        signup=signup,
        person_form=person_form,
        signup_form=signup_form,
        signup_extra_form=signup_extra_form
    )

    return render(request, 'labour_admin_signup_view.jade', vars)


@labour_admin_required
def labour_admin_signups_view(request, vars, event):
    signups = event.signup_set.all().order_by('person__surname', 'person__first_name')

    vars.update(
        signups=signups,
    )

    return render(request, 'labour_admin_signups_view.jade', vars)


def labour_admin_roster_vars(request, event):
    from programme.utils import full_hours_between

    hours = full_hours_between(event.labour_event_meta.work_begins, event.labour_event_meta.work_ends)

    return dict(
        hours=hours,
        num_hours=len(hours)
    )


@labour_admin_required
def labour_admin_roster_view(request, vars, event):
    vars.update(
        **labour_admin_roster_vars(request, event)
    )

    return render(request, 'labour_admin_roster_view.jade', vars)


@labour_admin_required
def labour_admin_roster_job_category_fragment(request, vars, event, job_category):
    job_category = get_object_or_404(JobCategory, event=event, pk=job_category)

    vars.update(
        **labour_admin_roster_vars(request, event)
    )

    hours = vars['hours']

    vars.update(
        job_category=job_category,
        totals=[0 for i in hours],
    )

    return json_response(dict(
        replace='#jobcategory-{0}-placeholder'.format(job_category.pk),
        content=render_string(request, 'labour_admin_roster_job_category_fragment.jade', vars)
    ))



def labour_admin_menu_items(request, event):
    dashboard_url = url('labour_admin_dashboard_view', event.slug)
    dashboard_active = request.path == dashboard_url
    dashboard_text = u"Kojelauta"

    signups_url = url('labour_admin_signups_view', event.slug)
    signups_active = request.path.startswith(signups_url)
    signups_text = u"Tapahtumaan ilmoittautuneet henkilöt"

    # roster_url = url('labour_admin_roster_view', event.slug)
    # roster_active = request.path == roster_url
    # roster_text = u"Työvuorojen suunnittelu"

    return [
        (dashboard_active, dashboard_url, dashboard_text),
        (signups_active, signups_url, signups_text),
        # (roster_active, roster_url, roster_text),
    ]
