# encoding: utf-8

from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404, render
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.http import require_http_methods

from core.utils import initialize_form
from core.tabs import Tab

from ..forms import (
    InvitationForm,
    ProgrammeAdditionalForm,
    ProgrammeInternalForm,
    ProgrammePublicForm,
    ScheduleForm,
)
from ..helpers import programme_admin_required
from ..models import Programme


@programme_admin_required
@require_http_methods(['GET', 'HEAD', 'POST'])
def programme_admin_detail_view(request, vars, event, programme_id):
    programme = get_object_or_404(Programme, category__event=event, pk=int(programme_id))

    public_form = initialize_form(ProgrammePublicForm, request, instance=programme, event=event, prefix='public')
    internal_form = initialize_form(ProgrammeInternalForm, request, instance=programme, event=event, prefix='internal')
    additional_form = initialize_form(ProgrammeAdditionalForm, request, instance=programme, event=event, prefix='additional')
    schedule_form = initialize_form(ScheduleForm, request, instance=programme, event=event, prefix='schedule')
    forms = [public_form, internal_form, schedule_form, additional_form]

    invitation_form = initialize_form(InvitationForm, request, prefix='invitation')

    if request.method == 'POST':
        action = request.POST.get('action')

        if action in ('save-edit', 'save-return'):
            if all(form.is_valid() for form in forms):
                for form in forms:
                    form.save()

                messages.success(request, _(u'The changes were saved.'))

                if action == 'save-edit':
                    return redirect('programme_admin_detail_view', event.slug, programme_id)
                elif action == 'save-return':
                    return redirect('programme_admin_view', event.slug)
                else:
                    raise NotImplementedError(action)
            else:
                messages.error(request, _(u'Please check the form.'))

        elif action == 'invite-host':
            if invitation_form.is_valid():
                invitation = invitation_form.save(commit=False)
                invitation.programme = programme
                invitation.save()

                messages.success(request, _(u'The host was successfully invited.'))

                return redirect('programme_admin_detail_view', event.slug, programme_id)
            else:
                messages.error(request, _(u'Please check the form.'))

        else:
            messages.error(request, _(u'Invalid action.'))

    tabs = [
        Tab('programme-admin-programme-public-tab', _(u'Public information'), active=True),
        Tab('programme-admin-programme-schedule-tab', _(u'Schedule information')),
        Tab('programme-admin-programme-internal-tab', _(u'Internal information')),
        Tab('programme-admin-programme-additional-tab', _(u'Additional information')),
        Tab('programme-admin-programme-hosts-tab', _(u'Programme hosts')),
    ]

    previous_programme, next_programme = programme.get_previous_and_next_programme()

    vars.update(
        additional_form=additional_form,
        internal_form=internal_form,
        invitation_form=invitation_form,
        invitations=programme.invitation_set.all(),
        next_programme=next_programme,
        overlapping_programmes=programme.get_overlapping_programmes(),
        previous_programme=previous_programme,
        programme=programme,
        programme_roles=programme.organizers.all(),
        public_form=public_form,
        schedule_form=schedule_form,
        tabs=tabs,
    )

    return render(request, 'programme_admin_detail_view.jade', vars)