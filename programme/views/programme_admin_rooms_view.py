from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.http import require_http_methods

from ..models import Room
from ..helpers import programme_admin_required
from ..forms import DeleteRoomForm


@programme_admin_required
@require_http_methods(["GET", "HEAD", "POST"])
def programme_admin_rooms_view(request, vars, event):
    rooms = Room.objects.filter(event=event)

    if request.method == 'POST':
        delete_room_form = DeleteRoomForm(request.POST, event=event)
        if delete_room_form.is_valid():
            delete_room_form.save()
            messages.success(request, _("The room was deleted."))
        else:
            messages.error(request, _("Invalid request."))

        return redirect('programme_admin_rooms_view', event.slug)

    vars.update(rooms=rooms)

    return render(request, 'programme_admin_rooms_view.pug', vars)
