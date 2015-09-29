# encoding: utf-8

from django.conf import settings
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from django.shortcuts import get_object_or_404

from dateutil.tz import tzlocal

from api.utils import api_view

from ..helpers import labour_admin_required, labour_event_required
from ..models import (
    JobCategory,
)



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
@api_view
def labour_api_set_job_requirement_view(request, vars, event, job_category_slug, job_slug):
    job_category = get_object_or_404(JobCategory, event=event, slug=job_category_slug)
    job = get_object_or_404(Job, job_category=job_category, slug=job_slug)

    params = SetJobRequirementRequest.from_dict(json.loads(request.body))

    start_time = dateutil.parse(params.start_time)
    end_time = start_time + timedelta(hours=params.hours)
