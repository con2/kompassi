from django.shortcuts import render

from backend.models import Room, Programme

def schedule_view(request):
    vars = dict(
      rooms=Room.objects.filter(public=True),
      programmes_by_start_time=Programme.programmes_by_start_time()
    )

    return render(request, 'programme.jade', vars)