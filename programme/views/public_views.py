# encoding: utf-8

from itertools import groupby
from datetime import datetime
import json

from dateutil.tz import tzlocal

from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template import RequestContext
from django.template.response import TemplateResponse
from django.template.loader import render_to_string
from django.utils.timezone import now
from django.views.decorators.cache import cache_page, cache_control
from django.views.decorators.http import require_http_methods, require_safe

from api.utils import api_view
from core.tabs import Tab
from core.utils import initialize_form, url

from ..models import (
    View,
    AllRoomsPseudoView,
    Category,
    Tag,
    Programme,
)
from ..helpers import programme_event_required, public_programme_required, group_programmes_by_start_time


def get_timetable_tabs(request, event):
    timetable_url = url('programme_timetable_view', event.slug)
    timetable_active = request.path == timetable_url
    timetable_text = u'Ohjelmakartta'

    special_url = url('programme_special_view', event.slug)
    special_active = request.path == special_url
    special_text = u'Ohjelmakartan ulkopuolinen ohjelma'

    return [
        Tab(timetable_url, timetable_text, timetable_active, 0),
        Tab(special_url, special_text, special_active, 0),
    ]


@public_programme_required
@cache_control(public=True, max_age=5 * 60)
@cache_page(5 * 60) # XXX remove once nginx cache is in place
@require_safe
def programme_timetable_view(
    request,
    event,
    internal_programmes=False,
    template='programme_timetable_view.jade',
):
    vars = dict(
        # hide the user menu to prevent it getting cached
        login_page=True,
        tabs=get_timetable_tabs(request, event),
    )

    return actual_timetable_view(request, event, internal_programmes, template, vars)

# look, no cache
@programme_event_required
@require_safe
def programme_internal_timetable_view(
    request,
    event,
    internal_programmes=True,
    template='programme_timetable_view.jade',
):
    vars = dict(
        tabs=get_timetable_tabs(request, event),
    )

    return actual_timetable_view(request, event, internal_programmes, template, vars)


def actual_timetable_view(
    request,
    event,
    internal_programmes=False,
    template='programme_timetable_view.jade',
    vars=None
):
    if not vars:
        vars = dict()

    all_rooms = AllRoomsPseudoView(event)

    category_query = dict(event=event)

    if not internal_programmes:
        category_query.update(public=True)

    vars.update(
        event=event,
        views=View.objects.filter(event=event, public=True),
        categories=Category.objects.filter(**category_query),
        internal_programmes=internal_programmes,
        programmes_by_start_time=all_rooms.get_programmes_by_start_time(request=request),
    )

    return render(request, template, vars)


@public_programme_required
@require_safe
def programme_special_view(request, event):
    return actual_special_view(request, event)


def actual_special_view(
        request,
        event,
        include_unpublished=False,
        template='programme_special_view.jade',
        vars=None
    ):
    programmes = event.programme_event_meta.get_special_programmes(
        include_unpublished=include_unpublished
    ).order_by('start_time')

    programmes_by_start_time = group_programmes_by_start_time(programmes)

    if vars is None:
        vars = dict()

    vars.update(
        tabs=get_timetable_tabs(request, event),
        event=event,
        programmes_by_start_time=programmes_by_start_time,
    )

    return render(request, template, vars)


@user_passes_test(lambda u: u.is_superuser)
@require_safe
def programme_internal_dumpdata_view(request):
    from django.core import management
    from cStringIO import StringIO

    buffer = StringIO()
    management.call_command('dumpdata', 'programme', stdout=buffer)
    response = HttpResponse(buffer.getvalue(), 'application/json')
    buffer.close()

    return response


@cache_control(public=True, max_age=1 * 60)
@cache_page(1 * 60) # XXX remove once nginx cache is in place
@public_programme_required
@require_safe
def programme_mobile_timetable_view(request, event):
    vars = dict(event=event)

    return render(request, 'programme_mobile_timetable.jade', vars)


@programme_event_required
@require_safe
def programme_internal_adobe_taggedtext_view(request, event):
    vars = dict(programmes_by_start_time=AllRoomsPseudoView(event).get_programmes_by_start_time(request=request))
    data = render_to_string('programme_timetable.taggedtext', vars, request=request)

    # force all line endings to CRLF (Windows)
    data = data.replace('\r\n', '\n').replace('\n', '\r\n')

    # encode to UTF-16; the LE at the end means no BOM, which is absolutely critical
    data = data.encode('UTF-16LE')

    return HttpResponse(data, 'text/plain; charset=utf-16')


@programme_event_required
@require_safe
@api_view
def programme_json_view(request, event, format='default'):
    result = []

    for start_time, incontinuity, row in AllRoomsPseudoView(event).get_programmes_by_start_time(request=request):
        for programme, rowspan in row:
            if programme is None:
                continue

            # TODO revise
            if format == 'desucon' and not programme.is_public:
                continue

            result.append(programme.as_json(format=format))

    return result


def programme_profile_menu_items(request):
    return []


def programme_event_box_context(request, event):
    return dict(
        is_programme_admin=event.programme_event_meta.is_user_admin(request.user),
    )
