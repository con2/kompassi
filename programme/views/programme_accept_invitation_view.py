# encoding: utf-8

from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render, get_object_or_404, redirect

from core.helpers import person_required
from core.utils import initialize_form

from ..forms import ProgrammeSelfServiceForm
from ..helpers import programme_event_required
from ..models.hosts import Invitation


@programme_event_required
@person_required
def programme_accept_invitation_view(request, event, code):
    invitation = get_object_or_404(Invitation, programme__category__event=event, code=code)
    programme = invitation.programme

    form = initialize_form(ProgrammeSelfServiceForm, request,
        instance=programme,
        event=event,
        prefix='needs',
    )

    if request.method == 'POST':
        if form.is_valid():
            invitation.accept(request.user.person)
            form.save()

            messages.success(request, _(u'Thank you for accepting the invitation. You can change the information later from your profile.'))

            # TODO once there is programme_profile_programme_view, go there instead
            return redirect('core_event_view', event.slug)
        else:
            messages.error(request, _(u'Please check the form.'))

    vars = dict(
        form=form,
    )

    return render(request, 'programme_accept_invitation_view.jade', vars)