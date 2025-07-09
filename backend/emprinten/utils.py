import typing

from django.http.response import HttpResponseBase

from .files import read_csv
from .models import Project
from .renderer import DataRow, render_pdf

__all__ = [
    "render_csv",
    "render_list",
    "render_obj",
]


def render_csv(
    project: Project,
    csv_io: typing.TextIO,
    *,
    return_archive: bool = False,
) -> tuple[HttpResponseBase, int]:
    data = read_csv(csv_io)
    return render_pdf(
        project.current_files(),
        project.name_pattern,
        project.title_pattern,
        data,
        return_archive=return_archive,
        handle_errors=True,
    ), len(data)


def render_list(
    project: Project,
    data: list[DataRow],
    *,
    return_archive: bool = False,
) -> HttpResponseBase:
    return render_pdf(
        project.current_files(),
        project.name_pattern,
        project.title_pattern,
        data,
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
