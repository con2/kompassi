# encoding: utf-8

from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages

from core.helpers import person_required
from core.utils import initialize_form

from ..forms import ProgrammeSelfServiceForm
from ..models import ProgrammeRole, Invitation, FreeformOrganizer
from ..proxies.programme.profile import ProgrammeProfileProxy


@person_required
def programme_profile_detail_view(request, programme_id):
    programme = get_object_or_404(ProgrammeProfileProxy, id=int(programme_id), organizers=request.user.person)
    event = programme.category.event

    form = initialize_form(ProgrammeSelfServiceForm, request,
        instance=programme,
        event=event,
        readonly=not programme.host_can_edit,
    )

    if request.method == 'POST':
        if not programme.host_can_edit:
            messages.error(request, programme.host_cannot_edit_explanation)
            return redirect('programme_profile_detail_view', programme.id)

        elif form.is_valid():
            form.save()
            messages.success(request, u'The changes were saved.')

            return redirect('programme_profile_view')

        else:
            messages.error(request, u'Please check the form.')

    vars = dict(
        event=event,
        form=form,
        freeform_organizers=FreeformOrganizer.objects.filter(programme=programme),
        invitations=Invitation.objects.filter(programme=programme, state='valid'),
        programme=programme,
        programme_roles=ProgrammeRole.objects.filter(programme=programme),
    )

    return render(request, 'programme_profile_detail_view.jade', vars)