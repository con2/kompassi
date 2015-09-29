# encoding: utf-8

from django.conf import settings
from django.views.decorators.http import require_http_methods, require_GET
from django.shortcuts import get_object_or_404

from dateutil.tz import tzlocal

from api.utils import api_view

from ..helpers import labour_admin_required, labour_event_required
from ..models import (
    JobCategory,
)



@require_GET
@labour_admin_required
@api_view
def labour_api_job_categories_view(request, vars, event):
    return [jc.as_dict() for jc in JobCategory.objects.filter(event=event, app_label='labour')]


@require_GET
@labour_admin_required
@api_view
def labour_api_job_category_view(request, vars, event, job_category_slug):
    return get_object_or_404(JobCategory, event=event, slug=job_category_slug).as_dict(include_jobs=True)
