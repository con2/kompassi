import logging
from datetime import timedelta

from dateutil.parser import parse as parse_datetime
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST, require_safe

from kompassi.api.utils import MethodNotAllowed, api_view
from kompassi.core.utils import full_hours_between

from ..helpers import labour_admin_required
from ..models import (
    EditJobRequest,
    EditShiftRequest,
    Job,
    JobCategory,
    JobRequirement,
    SetJobRequirementsRequest,
    Shift,
)

logger = logging.getLogger(__name__)


@labour_admin_required
@require_safe
@api_view
def api_job_categories_view(request, vars, event):
    return [jc.as_dict(include_requirements=True) for jc in JobCategory.objects.filter(event=event, app_label="labour")]


@labour_admin_required
@require_safe
@api_view
def api_job_category_view(request, vars, event, job_category_slug):
    return get_object_or_404(JobCategory, event=event, slug=job_category_slug).as_dict(
        include_jobs=True,
        include_shifts=True,
        include_people=True,
    )


@labour_admin_required
@api_view
def api_job_view(request, vars, event, job_category_slug, job_slug=None):
    job_category = get_object_or_404(JobCategory, event=event, slug=job_category_slug)

    if request.method == "POST" and job_slug is None:
        body = EditJobRequest.from_json(request.body)
        job = Job(job_category=job_category)
    elif request.method == "PUT" and job_slug is not None:
        body = EditJobRequest.from_json(request.body)
        job = get_object_or_404(Job, job_category=job_category, slug=job_slug)
    elif request.method == "DELETE" and job_slug is not None:
        job = get_object_or_404(Job, job_category=job_category, slug=job_slug)
        job.delete()
        return job_category.as_roster_api_dict()
    else:
        raise MethodNotAllowed(request.method)

    job.title = body.title
    job.save()

    return job_category.as_roster_api_dict()


@labour_admin_required
@api_view
def api_shift_view(request, vars, event, job_category_slug, shift_id=None):
    job_category = get_object_or_404(JobCategory, event=event, slug=job_category_slug)

    if request.method == "POST" and shift_id is None:
        shift = Shift()
        edit_shift_request = EditShiftRequest.from_json(request.body)
    elif request.method == "PUT" and shift_id is not None:
        shift = get_object_or_404(Shift, id=int(shift_id), job__job_category=job_category)
        edit_shift_request = EditShiftRequest.from_json(request.body)
    elif request.method == "DELETE" and shift_id is not None:
        shift = get_object_or_404(Shift, id=int(shift_id), job__job_category=job_category)
        shift.delete()
        return job_category.as_roster_api_dict()
    else:
        raise MethodNotAllowed(request.method)

    edit_shift_request.update(job_category, shift)
    shift.save()

    return job_category.as_roster_api_dict()


@labour_admin_required
@require_POST
@api_view
def api_set_job_requirements_view(request, vars, event, job_category_slug, job_slug):
    job_category = get_object_or_404(JobCategory, event=event, slug=job_category_slug)
    job = get_object_or_404(Job, job_category=job_category, slug=job_slug)

    body = SetJobRequirementsRequest.from_json(request.body)

    start_time = parse_datetime(body.startTime)
    end_time = start_time + timedelta(hours=body.hours - 1)  # -1 due to end parameter being inclusive

    start_time = max(start_time, event.labour_event_meta.work_begins)
    end_time = min(end_time, event.labour_event_meta.work_ends)

    for hour in full_hours_between(start_time, end_time):  # start/end inclusive
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
    return job_category.as_roster_api_dict()
