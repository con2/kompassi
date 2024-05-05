import http
import io
import typing

from django.contrib.auth.decorators import login_required
from django.core.files import File
from django.http import (
    HttpResponse,
    HttpResponseBase,
    HttpResponseForbidden,
)
from django.shortcuts import get_object_or_404, render
from django.utils.timezone import now
from django.views.decorators.http import require_POST
from jinja2 import exceptions

from .models import FileVersion, Project, RenderResult
from .utils import render_csv, render_obj
from .var_help import find_vars


@login_required
def project_index(request, event: str, slug: str) -> HttpResponse:
    project = get_object_or_404(Project, event__slug=event, slug=slug)

    if not project.is_allowed_to_supply_data(request.user):
        return HttpResponseForbidden()

    files = FileVersion.objects.filter(file__project=project, current=True).select_related("file")

    unusable = True
    required_vars = []
    template_error = None
    if files:
        project_vars = None
        try:
            # Find out referred row variables from template.
            # This will also catch some template errors.
            project_vars = find_vars(files, project.name_pattern, project.title_pattern)
        except exceptions.TemplateSyntaxError as e:
            template_error = str(e)
            if e.translated and (e.filename or e.name):
                # jinja2.debug.rewrite_traceback_stack sets translated on which hides source information.
                # Without traceback, the message doesn't make sense so add it manually.
                if not template_error.endswith("."):
                    template_error += "."
                template_error += f' File "{e.name or e.filename}", line {e.lineno}'
        except exceptions.TemplateError as e:
            template_error = str(e)
        except Exception:
            # Such as file backend connection problem; suppress the message for security.
            template_error = "Loading error"

        if project_vars is not None:
            unusable = False
            required_vars = sorted(project_vars)

    return render(
        request,
        "emprinten/generator_view.html",
        {
            "event_slug": event,
            "slug": project.slug,
            "title": project.name,
            "unusable": unusable,
            "template_error": template_error,
            "required_vars": required_vars,
            "is_zip": project.split_output,
        },
    )


@login_required
@require_POST
def handle_csv_upload(request, event: str, slug: str) -> HttpResponseBase:
    project = get_object_or_404(Project, event__slug=event, slug=slug)

    if not project.is_allowed_to_supply_data(request.user):
        return HttpResponseForbidden()

    csv_upload: File = request.FILES["file"]

    return_archive = project.split_output or request.POST.get("zip") is not None
    try:
        # csv_upload isn't strictly a buffer, but it is a binary file-like and needs to be interpreted as text.
        wrapped = io.TextIOWrapper(typing.cast(typing.BinaryIO, csv_upload), encoding="utf-8")
        start = now()
        result = render_csv(project, wrapped, return_archive=return_archive)
    except UnicodeDecodeError:
        return HttpResponse("Invalid text file supplied", status=http.HTTPStatus.BAD_REQUEST)

    RenderResult.objects.create(
        project=project,
        user=request.user,
        row_count=result[1],
        started=start,
    )
    return result[0]


@login_required
def handle_debug_request(request, slug: str) -> HttpResponseBase:
    project = get_object_or_404(Project, slug=slug)
    return render_obj(project, data=request.GET.dict())
