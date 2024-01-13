from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_http_methods, require_POST

from core.utils import initialize_form

from ..forms import (
    AddRoomForm,
    DeleteViewForm,
    MoveViewForm,
    MoveViewRoomForm,
    RemoveViewRoomForm,
    ViewForm,
)
from ..helpers import programme_admin_required
from ..models import View

schedule_actions = {
    "add-view": ViewForm,
    "move-view": MoveViewForm,
    "remove-room": RemoveViewRoomForm,
    "move-room": MoveViewRoomForm,
}


@programme_admin_required
@require_http_methods(["GET", "HEAD", "POST"])
def admin_schedule_view(request, vars, event):
    from .public_views import actual_schedule_view

    if request.method == "POST":
        action = request.POST.get("action")

        if action in schedule_actions:
            FormClass = schedule_actions[action]
            form = initialize_form(FormClass, request, event=event)
            if form.is_valid():
                form.save()
                messages.success(request, _("The schedule change was successful."))
                return redirect("programme:admin_schedule_view", event_slug=event.slug)
            else:
                messages.error(request, _("Please check the form."))
        else:
            messages.error(request, _("Unknown action"))

    vars.update(
        add_view_form=ViewForm(event=event),
    )

    return actual_schedule_view(
        request,
        event,
        internal_programmes=True,
        template="programme_admin_schedule_view.pug",
        vars=vars,
        show_programme_actions=True,
    )


view_actions = {
    "add-room": AddRoomForm,
    "update-view": ViewForm,
    "delete-view": DeleteViewForm,
}


@programme_admin_required
@require_POST
def admin_schedule_update_view_view(request, vars, event, view_id):
    view = get_object_or_404(View, id=int(view_id), event=event)
    action = request.POST.get("action")

    if action in view_actions:
        FormClass = view_actions[action]
        form = initialize_form(FormClass, request, instance=view)
        if form.is_valid():
            form.save()
            messages.success(request, _("The schedule change was successful."))
            return redirect("programme:admin_schedule_view", event_slug=event.slug)
        else:
            messages.error(request, _("Please check the form."))
    else:
        messages.error(request, _("Unknown action"))

    return redirect("programme:admin_schedule_view", event_slug=event.slug)
