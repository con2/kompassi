# encoding: utf-8

import logging
from pkg_resources import resource_string

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.http import require_http_methods, require_safe

from core.csv_export import csv_response, CSV_EXPORT_FORMATS, EXPORT_FORMATS, ExportFormat
from core.models import Person
from core.sort_and_filter import Filter, Sorter
from core.tabs import Tab
from core.utils import initialize_form, initialize_form_set, url

from ..models import (
    Category,
    Programme,
    ProgrammeEditToken,
    ProgrammeRole,
    Role,
    Room,
    STATE_CHOICES,
)
from ..helpers import programme_admin_required, group_programmes_by_start_time
from ..forms import (
    ProgrammePublicForm,
)


EXPORT_FORMATS = EXPORT_FORMATS + [
    ExportFormat(u'Tulostettava versio', 'html', 'html'),
]
logger = logging.getLogger('kompassi')


@programme_admin_required
def programme_admin_view(request, vars, event, format='screen'):
    programmes = Programme.objects.filter(category__event=event)

    categories = Category.objects.filter(event=event)
    category_filters = Filter(request, 'category').add_objects('category__slug', categories)
    programmes = category_filters.filter_queryset(programmes)

    rooms = Room.objects.filter(venue=event.venue)
    room_filters = Filter(request, 'room').add_objects('room__slug', rooms)
    programmes = room_filters.filter_queryset(programmes)

    state_filters = Filter(request, 'state').add_choices('state', STATE_CHOICES)
    state_filters.filter_queryset(programmes)
    programmes = state_filters.filter_queryset(programmes)

    if format != 'html':
        sorter = Sorter(request, 'sort')
        sorter.add('title', name='Otsikko', definition=('title',))
        sorter.add('start_time', name='Alkuaika', definition=('start_time','room'))
        sorter.add('room', name='Sali', definition=('room','start_time'))
        programmes = sorter.order_queryset(programmes)

    if format == 'screen':
        vars.update(
            category_filters=category_filters,
            export_formats=EXPORT_FORMATS,
            programmes=programmes,
            room_filters=room_filters,
            sorter=sorter,
            state_filters=state_filters,
        )

        return render(request, 'programme_admin_view.jade', vars)
    elif format in CSV_EXPORT_FORMATS:
        filename = "{event.slug}_programmes_{timestamp}.xlsx".format(
            event=event,
            timestamp=timezone.now().strftime('%Y%m%d%H%M%S'),
        )

        return csv_response(event, Programme, programmes,
            m2m_mode='comma_separated',
            dialect='xlsx',
            filename=filename,
        )
    elif format == 'html':
        title = u"{event_name}: Ohjelma".format(event_name=event.name)

        if room_filters.selected_slug != None:
            room = Room.objects.get(slug=room_filters.selected_slug)
            title += u' – {room.name}'.format(room=room)

        if state_filters.selected_slug != None:
            state_name = next(name for (slug, name) in STATE_CHOICES if slug == state_filters.selected_slug)
            title += u' ({state_name})'.format(state_name=state_name)

        programmes_by_start_time = group_programmes_by_start_time(programmes)

        vars.update(
            title=title,
            now=timezone.now(),
            programmes=programmes,
            programmes_by_start_time=programmes_by_start_time,
        )

        return render(request, 'programme_admin_print_view.jade', vars)
    else:
        raise NotImplementedError(format)


@programme_admin_required
@require_http_methods(['GET', 'HEAD', 'POST'])
def programme_admin_create_view(request, vars, event):
    form = initialize_form(ProgrammePublicForm, request, event=event)

    if request.method == 'POST':
        if form.is_valid():
            programme = form.save()
            messages.success(request, _(u'The programme was created.'))
            return redirect('programme_admin_detail_view', event.slug, programme.pk)
        else:
            messages.error(request, _(u'Please check the form.'))

    vars.update(
        form=form,
    )

    return render(request, 'programme_admin_create_view.jade', vars)


@programme_admin_required
@require_http_methods(['GET', 'HEAD', 'POST'])
def programme_admin_detail_view(request, vars, event, programme_id):
    programme = get_object_or_404(Programme, category__event=event, pk=int(programme_id))

    public_form = initialize_form(ProgrammePublicForm, request, instance=programme, event=event)

    tabs = [
        Tab('programme-admin-programme-public-tab', _(u'Public information'), active=True),
        Tab('programme-admin-programme-schedule-tab', _(u'Schedule information')),
        Tab('programme-admin-programme-hosts-tab', _(u'Programme hosts')),
        Tab('programme-admin-programme-internal-tab', _(u'Internal information')),
    ]

    vars.update(
        internal_form=public_form, # XXX
        overlapping_programmes=programme.get_overlapping_programmes(),
        public_form=public_form,
        schedule_form=public_form, # XXX
        add_host_form=public_form, # XXX
        tabs=tabs,
        programme=programme,
        previous_programme=None, # XXX
        next_programme=None, # XXX
    )

    return render(request, 'programme_admin_detail_view.jade', vars)


@programme_admin_required
@require_safe
def programme_admin_timetable_view(request, vars, event):
    from .public_views import actual_timetable_view

    return actual_timetable_view(
        request,
        event,
        internal_programmes=True,
        template='programme_admin_timetable_view.jade',
        vars=vars,
    )


@programme_admin_required
@require_safe
def programme_admin_special_view(request, vars, event):
    from .public_views import actual_special_view

    return actual_special_view(
        request,
        event,
        template='programme_admin_special_view.jade',
        vars=vars,
    )


def programme_admin_menu_items(request, event):
    timetable_url = url('programme_admin_timetable_view', event.slug)
    timetable_active = request.path == timetable_url
    timetable_text = u'Ohjelmakartan esikatselu'

    special_url = url('programme_admin_special_view', event.slug)
    special_active = request.path == special_url
    special_text = u'Ohjelmakartan ulkopuolisten esikatselu'

    index_url = url('programme_admin_view', event.slug)
    index_active = request.path.startswith(index_url) and not any((
        timetable_active,
        special_active,
    ))
    index_text = u'Ohjelmaluettelo'


    return [
        (index_active, index_url, index_text),
        (timetable_active, timetable_url, timetable_text),
        (special_active, special_url, special_text),
    ]


@programme_admin_required
def programme_admin_email_list_view(request, vars, event):
    addresses = Person.objects.filter(programme__category__event=event).order_by('email').values_list('email', flat=True).distinct()

    return HttpResponse("\n".join(addr for addr in addresses if addr), content_type='text/plain')
