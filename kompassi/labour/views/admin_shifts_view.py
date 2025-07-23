from django.shortcuts import render
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from kompassi.core.csv_export import CSV_EXPORT_FORMATS, EXPORT_FORMATS, ExportFormat, csv_response
from kompassi.core.sort_and_filter import Filter, Sorter

from ..helpers import labour_admin_required
from ..models import JobCategory, Shift

HTML_TEMPLATES = dict(
    screen="labour_admin_shifts_view.pug",
    html="labour_admin_shifts_print.pug",
)

EXPORT_FORMATS = [
    *EXPORT_FORMATS,
    ExportFormat("Tulostettava versio", "html", "html"),
]


@labour_admin_required
def admin_shifts_view(request, vars, event, format="screen"):
    shifts = (
        Shift.objects.filter(job__job_category__event=event)
        .select_related("signup__person")
        .select_related("job__job_category")
        .order_by("start_time", "signup__person__surname", "signup__person__first_name")
    )

    num_total_shifts = shifts.count()

    job_categories = JobCategory.objects.filter(event=event)
    job_category_filters = Filter(request, "category").add_objects("job__job_category__slug", job_categories)
    shifts = job_category_filters.filter_queryset(shifts)

    sorter = Sorter(request, "sort")
    sorter.add(
        "name",
        name="Nimen mukaan",
        definition=(
            "signup__person__surname",
            "signup__person__first_name",
            "start_time",
        ),
    )
    sorter.add(
        "job",
        name="Tehtävän mukaan",
        definition=(
            "job__job_category__name",
            "job__title",
            "start_time",
            "signup__person__surname",
            "signup__person__first_name",
        ),
    )
    sorter.add(
        "time",
        name="Alkuajan mukaan",
        definition=(
            "start_time",
            "signup__person__surname",
            "signup__person__first_name",
        ),
    )
    shifts = sorter.order_queryset(shifts)

    t = now()
    active_filter = job_category_filters.selected_definition

    if active_filter:
        title = _("{event_name}: Shift list – {job_category_name}").format(
            event_name=event.name,
            job_category_name=active_filter.name if active_filter else "Nimilista",
        )
    else:
        title = _("{event_name}: Shift list").format(
            event_name=event.name,
        )

    vars.update(
        active_filter=active_filter,
        export_formats=EXPORT_FORMATS,
        job_category_filters=job_category_filters,
        now=t,
        num_total_shifts=num_total_shifts,
        shifts=shifts,
        show_actions=(format == "screen"),
        sorter=sorter,
        title=title,
    )

    if format in HTML_TEMPLATES:
        template = HTML_TEMPLATES[format]
        return render(request, template, vars)
    elif format in CSV_EXPORT_FORMATS:
        filename = f"{event.slug}_shifts_{t.strftime('%Y%m%d%H%M%S')}.{format}"

        return csv_response(
            event,
            Shift,
            shifts,
            dialect=CSV_EXPORT_FORMATS[format],
            filename=filename,
            m2m_mode="separate_columns",
        )
    else:
        raise NotImplementedError(format)
