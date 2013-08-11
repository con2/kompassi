from django.shortcuts import render

from .models import View, AllRoomsPseudoView

def timetable_view(request):
    all_rooms = AllRoomsPseudoView()

    vars = dict(
        views=View.objects.filter(public=True),
        all_programmes_by_start_time=all_rooms.programmes_by_start_time
    )

    return render(request, 'timetable.jade', vars)