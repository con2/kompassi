# encoding: utf-8

import json
import logging
from datetime import datetime, timedelta

from django.conf import settings
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from dateutil.tz import tzlocal
from dateutil.parser import parse as parse_datetime

from api.utils import api_view
from core.utils import full_hours_between

from ..helpers import labour_admin_required, labour_event_required
from ..models import (
    Job,
    JobCategory,
    JobRequirement,
    SetJobRequirementsRequest
)


logger = logging.getLogger('kompassi')


@labour_admin_required
@require_GET
@api_view
def labour_api_job_categories_view(request, vars, event):
    return [
        jc.as_dict(include_requirements=True)
        for jc in JobCategory.objects.filter(event=event, app_label='labour')
    ]


@labour_admin_required
@require_GET
@api_view
def labour_api_job_category_view(request, vars, event, job_category_slug):
    return get_object_or_404(JobCategory, event=event, slug=job_category_slug).as_dict(include_jobs=True)


@labour_admin_required
@require_POST
@csrf_exempt
@api_view
def labour_api_set_job_requirements_view(request, vars, event, job_category_slug, job_slug):
    job_category = get_object_or_404(JobCategory, event=event, slug=job_category_slug)
    job = get_object_or_404(Job, job_category=job_category, slug=job_slug)

    params = SetJobRequirementsRequest.from_dict(json.loads(request.body))

    start_time = parse_datetime(params.startTime)
    end_time = start_time + timedelta(hours=params.hours)

    start_time = max(start_time, event.labour_event_meta.work_begins)
    end_time = min(end_time, event.labour_event_meta.work_ends)

    for hour in full_hours_between(start_time, end_time): # start/end inclusive
        requirement, created = JobRequirement.objects.get_or_create(
            job=job,
            start_time=hour,
            defaults=dict(
                count=params.required,
            ),
        )

        if not created:
            requirement.count = params.required
            requirement.save()

    # Successful result emulates that of /api/v1/events/tracon11/jobcategories/conitea
    return job_category.as_dict(include_jobs=True)
