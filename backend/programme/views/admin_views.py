import logging

from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone

from core.csv_export import CSV_EXPORT_FORMATS, EXPORT_FORMATS, ExportFormat, csv_response
from core.models import Person
from core.sort_and_filter import Filter, Sorter

from ..helpers import group_programmes_by_start_time, programme_admin_required
from ..models import (
    AlternativeProgrammeForm,
    Category,
    Programme,
    Room,
)
from ..models.programme import (
    PHOTOGRAPHY_CHOICES,
    STATE_CHOICES,
    VIDEO_PERMISSION_CHOICES,
)

EXPORT_FORMATS = [
    *EXPORT_FORMATS,
    ExportFormat("Tulostettava versio", "html", "html"),
]
logger = logging.getLogger("kompassi")


@programme_admin_required
def admin_view(request, vars, event, format="screen"):
    programmes = (
        Programme.objects.filter(category__event=event).select_related("category__event").select_related("room")
        # Does not do the needful due to formatted_organizers operating on the "through" model
        # .prefetch_related('organizers')
    )

    categories = Category.objects.filter(event=event)
    category_filters = Filter(request, "category").add_objects("category__slug", categories)
    programmes = category_filters.filter_queryset(programmes)

    rooms = event.rooms.all()
    room_filters = Filter(request, "room").add_objects("room__slug", rooms)
    programmes = room_filters.filter_queryset(programmes)

    state_filters = Filter(request, "state").add_choices("state", STATE_CHOICES)
    state_filters.filter_queryset(programmes)
    programmes = state_filters.filter_queryset(programmes)

    video_permission_filters = Filter(request, "video_permission")
    video_permission_filters.add_choices("video_permission", VIDEO_PERMISSION_CHOICES)
    programmes = video_permission_filters.filter_queryset(programmes)

    photography_filters = Filter(request, "photography").add_choices("photography", PHOTOGRAPHY_CHOICES)
    programmes = photography_filters.filter_queryset(programmes)

    forms = AlternativeProgrammeForm.objects.filter(event=event)
    if forms.exists():
        form_filters = Filter(request, "form_used").add_objects("form_used__slug", forms)
        programmes = form_filters.filter_queryset(programmes)
    else:
        form_filters = None

    if format != "html":
        sorter = Sorter(request, "sort")
        sorter.add("title", name="Otsikko", definition=("title",))
        sorter.add("start_time", name="Alkuaika", definition=("start_time", "room"))
        sorter.add("room", name="Sali", definition=("room", "start_time"))
        sorter.add("created_at", name="Uusin ensin", definition=("-created_at",))
        programmes = sorter.order_queryset(programmes)

    if event.slug.startswith("ropecon"):
        miniworkshop_filters = Filter(request, "ropecon_miniworkshop")
        miniworkshopinator = (
            lambda is_miniworkshop: lambda programme: programme.form_used
            and programme.form_used.slug == "tyopaja"
            and (programme.category.slug == "workmini") == is_miniworkshop
        )
        miniworkshop_filters.add("1", "Figutyöpajat", miniworkshopinator(True))
        miniworkshop_filters.add("0", "Työpajat, ei figut", miniworkshopinator(False))
        programmes = miniworkshop_filters.filter_queryset(programmes)
    else:
        miniworkshop_filters = None

    if format == "screen":
        vars.update(
            category_filters=category_filters,
            export_formats=EXPORT_FORMATS,
            form_filters=form_filters,
            miniworkshop_filters=miniworkshop_filters,
            photography_filters=photography_filters,
            programmes=programmes,
            room_filters=room_filters,
            sorter=sorter,
            state_filters=state_filters,
            video_permission_filters=video_permission_filters,
        )

        return render(request, "programme_admin_view.pug", vars)
    elif format in CSV_EXPORT_FORMATS:
        filename = "{event.slug}_programmes_{timestamp}.{format}".format(
            event=event,
            timestamp=timezone.now().strftime("%Y%m%d%H%M%S"),
            format=format,
        )

        return csv_response(
            event,
            Programme,
            programmes,
            m2m_mode="comma_separated",
            dialect=CSV_EXPORT_FORMATS[format],
            filename=filename,
        )
    elif format == "html":
        title = f"{event.name}: Ohjelma"

        if room_filters.selected_slug is not None:
            room = Room.objects.get(event=event, slug=room_filters.selected_slug)
            title += f" – {room.name}"

        if state_filters.selected_slug is not None:
            state_name = next(name for (slug, name) in STATE_CHOICES if slug == state_filters.selected_slug)
            title += f" ({state_name})"

        programmes_by_start_time = group_programmes_by_start_time(programmes)

        vars.update(
            title=title,
            now=timezone.now(),
            programmes=programmes,
            programmes_by_start_time=programmes_by_start_time,
        )

        return render(request, "programme_admin_print_view.pug", vars)
    else:
        raise NotImplementedError(format)


@programme_admin_required
def admin_email_list_view(request, vars, event):
    addresses = (
        Person.objects.filter(programme__category__event=event)
        .order_by("email")
        .values_list("email", flat=True)
        .distinct()
    )

    return HttpResponse("\n".join(addr for addr in addresses if addr), content_type="text/plain")
