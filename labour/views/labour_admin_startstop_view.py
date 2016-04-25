# encoding: utf-8

from __future__ import unicode_literals

from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.http import require_http_methods

from core.utils import initialize_form

from ..helpers import labour_admin_required
from ..forms import StartStopForm


@labour_admin_required
@require_http_methods(["GET", "HEAD", "POST"])
def labour_admin_startstop_view(request, vars, event):
    meta = event.labour_event_meta
    form = initialize_form(StartStopForm, request, instance=meta)

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'save':
            if form.is_valid():
                form.save()
                messages.success(request, _("Application period start and end times were saved."))
                return redirect("labour_admin_startstop_view", event.slug)
            else:
                messages.error(request, _("Please check the form."))

        elif action == 'start-now':
            if not meta.is_registration_open:
                meta.registration_opens = now()

                if meta.registration_closes <= meta.registration_closes:
                    messages.warning(request, _(
                        "The end of the application period was in the past and has now been cleared. "
                        "If you have an ending date for the application period, please set it below."
                    ))
                    meta.registration_closes = None

                meta.save()
                messages.success(request, _("The application period was started."))
            else:
                messages.error(request, _("The application period is already underway."))

            return redirect("labour_admin_startstop_view", event.slug)

        elif action == 'stop-now':
            if meta.is_registration_open:
                meta.registration_closes = now()
                meta.save()
                messages.success(request, _("The application period was ended."))
            else:
                messages.error(request, _("The application period is not currently underway."))

            return redirect("labour_admin_startstop_view", event.slug)

        else:
            messages.error(request, _("Invalid request."))

    vars.update(
        meta=meta,
        form=form,
    )

    return render(request, 'labour_admin_startstop_view.jade', vars)