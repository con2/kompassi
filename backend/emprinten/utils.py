import typing

from django.http.response import HttpResponseBase

from .files import read_csv
from .models import Project
from .renderer import DataRow, render_pdf

__all__ = [
    "render_csv",
    "render_obj",
]


def render_csv(
    project: Project,
    csv_io: typing.TextIO,
    *,
    return_archive: bool = False,
) -> HttpResponseBase:
    return render_pdf(
        project.current_files(),
        project.name_pattern,
        project.title_pattern,
        read_csv(csv_io),
        return_archive=return_archive,
    )


def render_obj(
    project: Project,
    data: DataRow,
) -> HttpResponseBase:
    return render_pdf(
        project.current_files(),
        project.name_pattern,
        project.title_pattern,
        [data],
        return_archive=False,
    )
