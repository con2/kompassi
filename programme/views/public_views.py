# encoding: utf-8

from datetime import datetime

from dateutil.tz import tzlocal

from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils.timezone import now
from django.views.decorators.cache import cache_page, cache_control
from django.views.decorators.http import require_http_methods, require_GET

from core.utils import render_string

from ..models import View, AllRoomsPseudoView, Category, Tag, Programme
from ..helpers import programme_event_required


@cache_control(public=True, max_age=5 * 60)
@cache_page(5 * 60) # XXX remove once nginx cache is in place
@programme_event_required
@require_GET
def programme_timetable_view(
    request,
    event,
    internal_programmes=False,
    template='programme_timetable_view.jade',
):
    return actual_timetable_view(request, event, internal_programmes, template)

# look, no cache
@programme_event_required
@require_GET
def programme_internal_timetable_view(
    request,
    event,
    internal_programmes=True,
    template='programme_timetable_view.jade',
):
    return actual_timetable_view(request, event, internal_programmes, template)


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
        all_programmes_by_start_time=all_rooms.programmes_by_start_time
    )

    return render(request, template, vars)


@user_passes_test(lambda u: u.is_superuser)
@require_GET
def programme_internal_dumpdata_view(request):
    from django.core import management
    from cStringIO import StringIO

    buffer = StringIO()
    management.call_command('dumpdata', 'timetable', stdout=buffer)
    response = HttpResponse(buffer.getvalue(), 'application/json')
    buffer.close()

    return response


@cache_control(public=True, max_age=1 * 60)
@cache_page(1 * 60) # XXX remove once nginx cache is in place
@programme_event_required
@require_GET
def programme_mobile_timetable_view(request, event):
    all_rooms = AllRoomsPseudoView(event)

    programmes_by_room = []
    for room in all_rooms.public_rooms:
        t = now()
        current_programme = room.programme_set.filter(start_time__lte=t, category__public=True).order_by('-start_time')[0:1]
        current_programme = current_programme[0] if current_programme else None
        ref_time = current_programme.end_time if current_programme else t

        next_programme = room.programme_set.filter(start_time__gte=ref_time, category__public=True).order_by('start_time')[0:1]
        next_programme = next_programme[0] if next_programme else None

        programmes_by_room.append((room, [("Nyt", current_programme), ("Seuraavaksi", next_programme)]))

    vars = dict(
        event=event,
        programmes_by_room=programmes_by_room
    )

    return render(request, 'programme_mobile_timetable.jade', vars)


@cache_control(public=True, max_age=1 * 60)
@cache_page(1 * 60) # XXX remove once nginx cache is in place
@programme_event_required
@require_GET
def programme_mobile_detail_view(request, event, programme_id):
    programme = get_object_or_404(Programme, category__event=event, id=programme_id)

    vars = dict(
        event=event,
        programme=programme,
    )

    return render(request, 'programme_mobile_detail.jade', vars)


@programme_event_required
@require_GET
def programme_internal_adobe_taggedtext_view(request, event):
    vars = dict(programmes_by_start_time=AllRoomsPseudoView(event).programmes_by_start_time)
    data = render_string(request, 'programme_timetable.taggedtext', vars)

    # force all line endings to CRLF (Windows)
    data = data.replace('\r\n', '\n').replace('\n', '\r\n')

    # encode to UTF-16; the LE at the end means no BOM, which is absolutely critical
    data = data.encode('UTF-16LE')

    return HttpResponse(data, 'text/plain; charset=utf-16')


@programme_event_required
@require_http_methods(['GET', 'POST'])
def programme_self_service_view(request, event, programme_edit_code):
    token = get_object_or_404(ProgrammeEditToken,
        programme__category__event=event,
        code=programme_edit_code
    )

    programme_form = initialize_form(ProgrammeForm, request,
        instance=token.programme,
    )

    vars = dict(
        programme_form=programme_form,
        login_page=True # XXX
    )

    if request.method == 'POST':
        if programme_form.is_valid():
            programme_form.save()
            messages.success(u'Ohjelmanumerosi tiedot tallennettiin.')

    return render(request, 'programme_self_service_view.jade', vars)


def programme_profile_menu_items(request):
    return []


def programme_event_box_context(request, event):
    return dict()
