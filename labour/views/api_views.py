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

from api.utils import api_view, MethodNotAllowed
from core.utils import full_hours_between

from ..helpers import labour_admin_required, labour_event_required
from ..models import (
    Job,
    JobCategory,
    JobRequirement,
    SetJobRequirementsRequest,
    EditJobRequest,
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
@api_view
def labour_api_job_view(request, vars, event, job_category_slug, job_slug=None):
    job_category = get_object_or_404(JobCategory, event=event, slug=job_category_slug)

    if request.method == 'POST' and job_slug is None:
        body = EditJobRequest.from_json(request.body)
        job = Job(job_category=job_category)
    elif request.method == 'PUT' and job_slug is not None:
        body = EditJobRequest.from_json(request.body)
        job = get_object_or_404(Job, job_category=job_category, slug=job_slug)
    elif request.method == 'DELETE' and job_slug is not None:
        job = get_object_or_404(Job, job_category=job_category, slug=job_slug)
        job.delete()
        return job_category.as_dict(include_jobs=True)
    else:
        raise MethodNotAllowed(request.method)

    job.title = body.title
    job.save()

    return job_category.as_dict(include_jobs=True)

@labour_admin_required
@require_POST
@api_view
def labour_api_set_job_requirements_view(request, vars, event, job_category_slug, job_slug):
    job_category = get_object_or_404(JobCategory, event=event, slug=job_category_slug)
    job = get_object_or_404(Job, job_category=job_category, slug=job_slug)

    body = SetJobRequirementsRequest.from_json(request.body)

    start_time = parse_datetime(body.startTime)
    end_time = start_time + timedelta(hours=body.hours - 1) # -1 due to end parameter being inclusive

    start_time = max(start_time, event.labour_event_meta.work_begins)
    end_time = min(end_time, event.labour_event_meta.work_ends)

    for hour in full_hours_between(start_time, end_time): # start/end inclusive
        requirement, created = JobRequirement.objects.get_or_create(
            job=job,
            start_time=hour,
            defaults=dict(
                count=body.required,
            ),
        )

        if not created:
            requirement.count = body.required
            requirement.save()

    # Successful result emulates that of /api/v1/events/tracon11/jobcategories/conitea
    return job_category.as_dict(include_jobs=True)
