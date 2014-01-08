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

from .models import View, AllRoomsPseudoView, Category, Tag, Programme

@cache_control(public=True, max_age=5 * 60)
@cache_page(5 * 60) # XXX remove once nginx cache is in place
def timetable_view(request):
    return render_timetable(request, internal_programmes=False)

def render_timetable(request, internal_programmes=False):
    all_rooms = AllRoomsPseudoView()

    if internal_programmes:
        category_query = dict()
    else:
        category_query = dict(public=True)

    vars = dict(
        views=View.objects.filter(public=True),
        categories=Category.objects.filter(**category_query),
        internal_programmes=internal_programmes,
        all_programmes_by_start_time=all_rooms.programmes_by_start_time
    )

    return render(request, 'timetable.jade', vars)


@user_passes_test(lambda u: u.is_superuser)
def internal_dumpdata_view(request):
    from django.core import management
    from cStringIO import StringIO

    buffer = StringIO()
    management.call_command('dumpdata', 'timetable', stdout=buffer)
    response = HttpResponse(buffer.getvalue(), 'application/json')
    buffer.close()

    return response

@cache_control(public=True, max_age=1 * 60)
@cache_page(1 * 60) # XXX remove once nginx cache is in place
def mobile_timetable_view(request):
    all_rooms = AllRoomsPseudoView()

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
        programmes_by_room=programmes_by_room
    )

    return render(request, 'mobile_timetable.jade', vars)

@cache_control(public=True, max_age=1 * 60)
@cache_page(1 * 60) # XXX remove once nginx cache is in place
def mobile_programme_detail_view(request, programme_id):
    programme = get_object_or_404(Programme, id=programme_id)

    vars = dict(
        programme=programme
    )

    return render(request, 'mobile_programme_detail.jade', vars)


#@login_required
def internal_timetable_view(request):
    return render_timetable(request, internal_programmes=True)


#@login_required
def internal_adobe_taggedtext_view(request):
    vars = dict(programmes_by_start_time=AllRoomsPseudoView().programmes_by_start_time)
    data = render_to_string('timetable.taggedtext', vars, RequestContext(request, {}))

    # force all line endings to CRLF (Windows)
    data = data.replace('\r\n', '\n').replace('\n', '\r\n')

    # encode to UTF-16; the LE at the end means no BOM, which is absolutely critical
    data = data.encode('UTF-16LE')

    return HttpResponse(data, 'text/plain; charset=utf-16')