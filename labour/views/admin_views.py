# encoding: utf-8

from collections import Counter, OrderedDict, namedtuple
import json

import datetime

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db.models.query import Q
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
def labour_admin_dashboard_view(request, vars, event):
    vars.update(
        # XXX state overhaul
        num_pending=event.signup_set.filter(is_active=True, time_accepted__isnull=True).count(),
        num_accepted=event.signup_set.filter(time_accepted__isnull=False).count(),
        num_rejected=event.signup_set.filter(Q(time_rejected__isnull=False) | Q(time_cancelled__isnull=False)).count(),
        signups=event.signup_set.order_by('-created_at')[:5]
    )

    return render(request, 'labour_admin_dashboard_view.pug', vars)


@labour_admin_required
def labour_admin_roster_view(request, vars, event, job_category_slug=None):
    if job_category_slug is not None:
        get_object_or_404(JobCategory, event=event, slug=job_category_slug)

    tz = tzlocal()

    # use javaScriptCase because this gets directly embedded in <script> as json
    config = dict(
        event=event.as_dict(),
        workHours=[
            dict(startTime=hour.astimezone(tz).isoformat())
            for hour in event.labour_event_meta.work_hours
        ],
        lang='fi', # XXX I18N hardcoded
        urls=dict(
            base=url('labour_admin_roster_view', event.slug),
            jobCategoryApi=url('labour_api_job_categories_view', event.slug),
        )
    )

    vars.update(
        config_json=json.dumps(config),
    )

    return render(request, 'labour_admin_roster_view.pug', vars)


@labour_admin_required
@require_safe
def labour_admin_mail_view(request, vars, event):
    from mailings.models import Message

    messages = Message.objects.filter(recipient__event=event, recipient__app_label='labour')

    vars.update(
        labour_messages=messages
    )

    return render(request, 'labour_admin_mail_view.pug', vars)
