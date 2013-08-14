from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test

from .models import View, AllRoomsPseudoView

def timetable_view(request):
    return render_timetable(request, internal_programmes=False)

def render_timetable(request, internal_programmes=False):
    all_rooms = AllRoomsPseudoView()

    vars = dict(
        views=View.objects.filter(public=True),
        internal_programmes=internal_programmes,
        all_programmes_by_start_time=all_rooms.programmes_by_start_time
    )

    return render(request, 'timetable.jade', vars)

@user_passes_test(lambda u: u.is_superuser)
def internal_dumpdata_view(request):
    from django.core import management
    from django.http import HttpResponse
    import cStringIO as StringIO

    s = StringIO.StringIO()
    management.call_command('dumpdata', 'timetable', stdout=s)
    r = HttpResponse(s.getvalue(), 'application/json')
    s.close()

    return r

#@login_required
def internal_timetable_view(request):
    return render_timetable(request, internal_programmes=True)