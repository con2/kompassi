from django.contrib.auth.decorators import login_required
from django.http import (
    HttpResponseBase,
)
from django.shortcuts import get_object_or_404

from .models import Project
from .utils import render_obj


@login_required
def handle_debug_request(request, slug: str) -> HttpResponseBase:
    project = get_object_or_404(Project, slug=slug)
    return render_obj(project, data=request.GET.dict())
