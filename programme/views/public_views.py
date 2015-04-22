# encoding: utf-8

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
from django.views.decorators.http import require_http_methods, require_GET

from api.utils import api_view
from core.utils import render_string, initialize_form

from ..models import (
    View,
    AllRoomsPseudoView,
    Category,
    Tag,
    Programme,
    ProgrammeEditToken,
)
from ..helpers import programme_event_required, public_programme_required

@public_programme_required
@cache_control(public=True, max_age=5 * 60)
@cache_page(5 * 60) # XXX remove once nginx cache is in place
@require_GET
def programme_timetable_view(
    request,
    event,
    internal_programmes=False,
    template='programme_timetable_view.jade',
):
    vars = dict(
        # hide the user menu to prevent it getting cached
        login_page=True,
    )

    return actual_timetable_view(request, event, internal_programmes, template, vars)

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
    management.call_command('dumpdata', 'programme', stdout=buffer)
    response = HttpResponse(buffer.getvalue(), 'application/json')
    buffer.close()

    return response


@cache_control(public=True, max_age=1 * 60)
@cache_page(1 * 60) # XXX remove once nginx cache is in place
@public_programme_required
@require_GET
def programme_mobile_timetable_view(request, event):
    vars = dict(event=event)

    return render(request, 'programme_mobile_timetable.jade', vars)


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
@require_GET
def programme_internal_konopas_javascript_view(request, event):
    program = []
    people = {}

    for programme in Programme.objects.filter(
        category__event=event,
        category__public=True,
        start_time__isnull=False,
        room__isnull=False,
    ):
        program.append(dict(
            id=str(programme.pk),
            title=programme.title,
            tags=[programme.category.title],
            date=programme.local_start_time.strftime("%Y-%m-%d"),
            time=programme.local_start_time.strftime("%H:%M"),
            mins=programme.length,
            loc=[programme.room.name],
            people=[dict(
                id=person.pk,
                name=person.display_name,
            ) for person in programme.organizers.all()],
            desc=programme.description,
        ))

        for person in programme.organizers.all():
            if person.preferred_name_display_style == 'nick':
                name_list = [person.nick, "", "", ""]
            else:
                name_list = [person.surname, person.first_name, "", ""]

            people[str(person.pk)] = dict(
                id=str(person.pk),
                name=name_list,
                tags=[],
                prog=[str(prog.pk) for prog in person.programme_set.filter(
                    category__event=event,
                    category__public=True,
                    start_time__isnull=False,
                    room__isnull=False,
                )],
                links={},
                bio="",
            )

    context = RequestContext(request, dict(
        program=json.dumps(program),
        people=json.dumps(people),
    ))

    return TemplateResponse(request, 'programme_internal_konopas_javascript_view.js',
        context=context,
        content_type='application/javascript',
    )


@programme_event_required
@require_http_methods(['GET', 'POST'])
def programme_self_service_view(request, event, programme_edit_code):
    token = get_object_or_404(ProgrammeEditToken,
        programme__category__event=event,
        code=programme_edit_code
    )

    token.used_at = now()
    token.save()

    programme = token.programme

    from .admin_views import actual_detail_view

    vars = dict(
        event=event,
        login_page=True, # XXX
    )

    return actual_detail_view(request, vars, event, programme,
        template='programme_self_service_view.jade',
        self_service=True,
        redirect_success=lambda ev, unused: redirect('programme_self_service_view', ev.slug, token.code),
    )


@programme_event_required
@require_GET
@api_view
def programme_json_view(request, event, format='default'):
    result = []

    for start_time, incontinuity, row in AllRoomsPseudoView(event).programmes_by_start_time:
        for programme, rowspan in row:
            if programme is None:
                continue

            # TODO revise
            if format == 'desucon' and not programme.public:
                continue

            result.append(programme.as_json(format=format))

    return result


def programme_profile_menu_items(request):
    return []


def programme_event_box_context(request, event):
    return dict(
        is_programme_admin=event.programme_event_meta.is_user_admin(request.user),
    )
