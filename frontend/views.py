from django.shortcuts import render

from backend.models import Room

from .models import View, AllRoomsPseudoView

def schedule_view(request):
    all_rooms = AllRoomsPseudoView()

    vars = dict(
        views=View.objects.filter(public=True),
        all_programmes_by_start_time=all_rooms.programmes_by_start_time
    )

    return render(request, 'schedule.jade', vars)