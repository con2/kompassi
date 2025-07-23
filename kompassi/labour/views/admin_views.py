import json

from dateutil.tz import tzlocal
from django.db.models.query import Q
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_safe

from kompassi.core.utils import url

from ..helpers import labour_admin_required
from ..models import (
    JobCategory,
)


@labour_admin_required
def admin_dashboard_view(request, vars, event):
    vars.update(
        # XXX state overhaul
        num_pending=event.signup_set.filter(is_active=True, time_accepted__isnull=True).count(),
        num_accepted=event.signup_set.filter(time_accepted__isnull=False).count(),
        num_rejected=event.signup_set.filter(Q(time_rejected__isnull=False) | Q(time_cancelled__isnull=False)).count(),
        signups=event.signup_set.order_by("-created_at")[:5],
    )

    return render(request, "labour_admin_dashboard_view.pug", vars)


@labour_admin_required
def admin_roster_view(request, vars, event, job_category_slug=None):
    if job_category_slug is not None:
        get_object_or_404(JobCategory, event=event, slug=job_category_slug)

    tz = tzlocal()

    # use javaScriptCase because this gets directly embedded in <script> as json
    config = dict(
        event=event.as_dict(),
        workHours=[dict(startTime=hour.astimezone(tz).isoformat()) for hour in event.labour_event_meta.work_hours],
        lang="fi",  # XXX I18N hardcoded
        urls=dict(
            base=url("labour:admin_roster_view", event.slug),
            jobCategoryApi=url("labour:api_job_categories_view", event.slug),
        ),
    )

    vars.update(
        config_json=json.dumps(config),
        disable_feedback_widget=True,
    )

    return render(request, "labour_admin_roster_view.pug", vars)


@labour_admin_required
@require_safe
def admin_mail_view(request, vars, event):
    from kompassi.mailings.models import Message

    messages = Message.objects.filter(recipient__event=event, recipient__app_label="labour")

    vars.update(not_messages=messages)

    return render(request, "labour_admin_mail_view.pug", vars)
