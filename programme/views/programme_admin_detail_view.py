# encoding: utf-8

from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404, render
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.http import require_http_methods

from core.utils import initialize_form
from core.tabs import Tab

from ..forms import (
    FreeformOrganizerForm,
    InvitationForm,
    ProgrammeInternalForm,
    ProgrammeNeedsForm,
    ProgrammePublicForm,
    ScheduleForm,
)
from ..helpers import programme_admin_required
from ..models import (
    FreeformOrganizer,
    Invitation,
    ProgrammeRole,
)
from ..proxies.programme.management import ProgrammeManagementProxy


@programme_admin_required
@require_http_methods(['GET', 'HEAD', 'POST'])
def programme_admin_detail_view(request, vars, event, programme_id):
    programme = get_object_or_404(ProgrammeManagementProxy, category__event=event, pk=int(programme_id))

    public_form = initialize_form(ProgrammePublicForm, request, instance=programme, event=event, prefix='public')
    needs_form = initialize_form(ProgrammeNeedsForm, request, instance=programme, event=event, prefix='needs')
    internal_form = initialize_form(ProgrammeInternalForm, request, instance=programme, event=event, prefix='internal')
    schedule_form = initialize_form(ScheduleForm, request, instance=programme, event=event, prefix='schedule')
    forms = [public_form, needs_form, schedule_form, internal_form]

    invitation_form = initialize_form(InvitationForm, request, event=event, prefix='invitation')
    freeform_organizer_form = initialize_form(FreeformOrganizerForm, request, prefix='freeform')

    if request.method == 'POST':
        action = request.POST.get('action')

        if action in ('save-edit', 'save-return'):
            if all(form.is_valid() for form in forms):
                for form in forms:
                    form.save()

                programme.apply_state()

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
                invitation.created_by = request.user
                invitation.save()

                invitation.send(request)

                messages.success(request, _(u'The host was successfully invited.'))

                return redirect('programme_admin_detail_view', event.slug, programme_id)
            else:
                messages.error(request, _(u'Please check the form.'))

        elif action == 'add-freeform-host':
            if freeform_organizer_form.is_valid():
                freeform_organizer_form = freeform_organizer_form.save(commit=False)
                freeform_organizer_form.programme = programme
                freeform_organizer_form.save()

                messages.success(request, _(u'The freeform organizer was successfully added.'))

                return redirect('programme_admin_detail_view', event.slug, programme_id)
            else:
                messages.error(request, _(u'Please check the form.'))

        elif (
            action.startswith('remove-host:') or
            action.startswith('remove-freeform-host:') or
            action.startswith('cancel-invitation:')
        ):
            action, id_str = action.split(':', 1)

            try:
                id_int = int(id_str)
            except ValueError:
                messages.error(request, _(u'Invalid action.'))
            else:
                if action == 'remove-host':
                    programme_role = get_object_or_404(ProgrammeRole, id=id_int, programme=programme)
                    programme_role.delete()

                    programme.apply_state(deleted_programme_roles=programme_role)

                    messages.success(request, _(u'The host was removed.'))
                elif action == 'cancel-invitation':
                    invitation = get_object_or_404(Invitation, id=id_int, programme=programme, state='valid')
                    invitation.state = 'revoked'
                    invitation.save()

                    programme.apply_state()

                    messages.success(request, _(u'The invitation was cancelled.'))
                elif action == 'remove-freeform-host':
                    freeform_organizer = get_object_or_404(FreeformOrganizer, id=id_int, programme=programme)
                    freeform_organizer.delete()

                    programme.apply_state()

                    messages.success(request, _(u'The host was removed.'))
                else:
                    raise NotImplementedError(action)

                return redirect('programme_admin_detail_view', event.slug, programme_id)
        else:
            messages.error(request, _(u'Invalid action.'))

    tabs = [
        Tab('programme-admin-programme-public-tab', _(u'Public information'), active=True),
        Tab('programme-admin-programme-schedule-tab', _(u'Schedule information')),
        Tab('programme-admin-programme-needs-tab', _(u'Host needs')),
        Tab('programme-admin-programme-internal-tab', _(u'Internal information')),
        Tab('programme-admin-programme-hosts-tab', _(u'Programme hosts')),
    ]

    previous_programme, next_programme = programme.get_previous_and_next_programme()

    vars.update(
        freeform_organizers=FreeformOrganizer.objects.filter(programme=programme),
        freeform_organizer_form=freeform_organizer_form,
        internal_form=internal_form,
        invitation_form=invitation_form,
        invitations=programme.invitation_set.filter(state='valid'),
        needs_form=needs_form,
        next_programme=next_programme,
        overlapping_programmes=programme.get_overlapping_programmes(),
        previous_programme=previous_programme,
        programme=programme,
        programme_roles=ProgrammeRole.objects.filter(programme=programme),
        public_form=public_form,
        schedule_form=schedule_form,
        tabs=tabs,
    )

    return render(request, 'programme_admin_detail_view.jade', vars)