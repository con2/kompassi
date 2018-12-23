import logging

from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.http import require_safe

from core.csv_export import csv_response, CSV_EXPORT_FORMATS, EXPORT_FORMATS, ExportFormat
from core.models import Person
from core.sort_and_filter import Filter, Sorter

from ..models import (
    AlternativeProgrammeForm,
    Category,
    Programme,
    Room,
)
from ..models.programme import (
    STATE_CHOICES,
    VIDEO_PERMISSION_CHOICES,
    PHOTOGRAPHY_CHOICES,
)
from ..helpers import programme_admin_required, group_programmes_by_start_time


EXPORT_FORMATS = EXPORT_FORMATS + [
    ExportFormat('Tulostettava versio', 'html', 'html'),
]
logger = logging.getLogger('kompassi')


@programme_admin_required
def programme_admin_view(request, vars, event, format='screen'):
    programmes = (
        Programme.objects.filter(category__event=event)
        .select_related('category__event')
        .select_related('room')

        # Does not do the needful due to formatted_organizers operating on the "through" model
        # .prefetch_related('organizers')
    )

    categories = Category.objects.filter(event=event)
    category_filters = Filter(request, 'category').add_objects('category__slug', categories)
    programmes = category_filters.filter_queryset(programmes)

    rooms = event.rooms.all()
    room_filters = Filter(request, 'room').add_objects('room__slug', rooms)
    programmes = room_filters.filter_queryset(programmes)

    state_filters = Filter(request, 'state').add_choices('state', STATE_CHOICES)
    state_filters.filter_queryset(programmes)
    programmes = state_filters.filter_queryset(programmes)

    video_permission_filters = Filter(request, 'video_permission')
    video_permission_filters.add_choices('video_permission', VIDEO_PERMISSION_CHOICES)
    video_permission_filters.filter_queryset(programmes)
    programmes = video_permission_filters.filter_queryset(programmes)

    photography_filters = Filter(request, 'photography').add_choices('photography', PHOTOGRAPHY_CHOICES)
    photography_filters.filter_queryset(programmes)
    programmes = photography_filters.filter_queryset(programmes)

    forms = AlternativeProgrammeForm.objects.filter(event=event)
    if forms.exists():
        form_filters = Filter(request, 'form_used').add_objects('form_used__slug', forms)
        programmes = form_filters.filter_queryset(programmes)
    else:
        form_filters = None

    if format != 'html':
        sorter = Sorter(request, 'sort')
        sorter.add('title', name='Otsikko', definition=('title',))
        sorter.add('start_time', name='Alkuaika', definition=('start_time', 'room'))
        sorter.add('room', name='Sali', definition=('room', 'start_time'))
        sorter.add('created_at', name='Uusin ensin', definition=('-created_at',))
        programmes = sorter.order_queryset(programmes)

    if format == 'screen':
        vars.update(
            category_filters=category_filters,
            export_formats=EXPORT_FORMATS,
            form_filters=form_filters,
            photography_filters=photography_filters,
            programmes=programmes,
            room_filters=room_filters,
            sorter=sorter,
            state_filters=state_filters,
            video_permission_filters=video_permission_filters,
        )

        return render(request, 'programme_admin_view.pug', vars)
    elif format in CSV_EXPORT_FORMATS:
        filename = "{event.slug}_programmes_{timestamp}.{format}".format(
            event=event,
            timestamp=timezone.now().strftime('%Y%m%d%H%M%S'),
            format=format,
        )

        return csv_response(event, Programme, programmes,
            m2m_mode='comma_separated',
            dialect=CSV_EXPORT_FORMATS[format],
            filename=filename,
        )
    elif format == 'html':
        title = "{event_name}: Ohjelma".format(event_name=event.name)

        if room_filters.selected_slug is not None:
            room = Room.objects.get(event=event, slug=room_filters.selected_slug)
            title += ' – {room.name}'.format(room=room)

        if state_filters.selected_slug is not None:
            state_name = next(name for (slug, name) in STATE_CHOICES if slug == state_filters.selected_slug)
            title += ' ({state_name})'.format(state_name=state_name)

        programmes_by_start_time = group_programmes_by_start_time(programmes)

        vars.update(
            title=title,
            now=timezone.now(),
            programmes=programmes,
            programmes_by_start_time=programmes_by_start_time,
        )

        return render(request, 'programme_admin_print_view.pug', vars)
    else:
        raise NotImplementedError(format)


@programme_admin_required
@require_safe
def programme_admin_special_view(request, vars, event):
    from .public_views import actual_special_view

    return actual_special_view(
        request,
        event,
        template='programme_admin_special_view.pug',
        vars=vars,
        show_programme_actions=True,
    )


@programme_admin_required
def programme_admin_email_list_view(request, vars, event):
    addresses = (
        Person.objects.filter(programme__category__event=event)
        .order_by('email')
        .values_list('email', flat=True)
        .distinct()
    )

    return HttpResponse("\n".join(addr for addr in addresses if addr), content_type='text/plain')
