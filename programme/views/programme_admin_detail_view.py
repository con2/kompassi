from collections import namedtuple

from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404, render
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.http import require_http_methods, require_POST

from core.utils import initialize_form
from core.tabs import Tab

from ..forms import (
    ChangeHostRoleForm,
    ChangeInvitationRoleForm,
    FreeformOrganizerForm,
    InvitationForm,
    IsUsingPaikkalaForm,
    PaikkalaProgramForm,
    ProgrammeInternalForm,
    ProgrammeSelfServiceForm,
    ScheduleForm,
)
from ..helpers import programme_admin_required
from ..models import (
    FreeformOrganizer,
    Invitation,
    ProgrammeRole,
)
from ..proxies.programme.management import ProgrammeManagementProxy


PerHostForms = namedtuple('PerHostForms', 'change_host_role_form signup_extra_form')


# TODO Split this into multiple views or at refactor it into a CBV
@programme_admin_required
@require_http_methods(['GET', 'HEAD', 'POST'])
def programme_admin_detail_view(request, vars, event, programme_id):
    programme = get_object_or_404(ProgrammeManagementProxy, category__event=event, pk=int(programme_id))

    if programme.form_used:
        FormClass = programme.form_used.programme_form_class
    else:
        FormClass = ProgrammeSelfServiceForm

    programme_form = initialize_form(FormClass, request, instance=programme, event=event, prefix='programme')
    internal_form = initialize_form(ProgrammeInternalForm, request, instance=programme, event=event, prefix='internal')
    schedule_form = initialize_form(ScheduleForm, request, instance=programme, event=event, prefix='schedule')
    is_using_paikkala_form = initialize_form(IsUsingPaikkalaForm, request,
        instance=programme,
        prefix='usepaikkala',
        disabled=not programme.can_paikkalize,
    )
    forms = [programme_form, schedule_form, internal_form, is_using_paikkala_form]

    if programme.is_using_paikkala and programme.paikkala_program:
        paikkala_program_form = initialize_form(PaikkalaProgramForm, request, instance=programme.paikkala_program, prefix='paikkala')
        forms.append(paikkala_program_form)
    else:
        paikkala_program_form = None

    invitation_form = initialize_form(InvitationForm, request, event=event, prefix='invitation')
    freeform_organizer_form = initialize_form(FreeformOrganizerForm, request, prefix='freeform')

    SignupExtra = event.programme_event_meta.signup_extra_model
    if SignupExtra.supports_programme:
        SignupExtraForm = SignupExtra.get_programme_form_class()
    else:
        SignupExtraForm = None

    programme_roles = ProgrammeRole.objects.filter(programme=programme)
    forms_per_host = []
    for role in programme_roles:
        change_host_role_form = initialize_form(ChangeHostRoleForm, request, prefix='chr', instance=role, event=event)
        if SignupExtraForm is not None:
            signup_extra_form = initialize_form(SignupExtraForm, request,
                prefix='sex',
                instance=SignupExtra.for_event_and_person(event, role.person)
            )
        else:
            signup_extra_form = None

        forms_per_host.append(PerHostForms(
            change_host_role_form=change_host_role_form,
            signup_extra_form=signup_extra_form,
        ))

    change_invitation_role_forms = [
        initialize_form(ChangeInvitationRoleForm, request, prefix='cir', instance=invitation, event=event)
        for invitation in programme.invitation_set.all()
    ]

    if request.method == 'POST':
        action = request.POST.get('action')

        if action in ('save-edit', 'save-return'):
            if all(form.is_valid() for form in forms):
                for form in forms:
                    form.save()

                programme.apply_state()

                messages.success(request, _('The changes were saved.'))

                if action == 'save-edit':
                    return redirect('programme_admin_detail_view', event.slug, programme_id)
                elif action == 'save-return':
                    return redirect('programme_admin_view', event.slug)
                else:
                    raise NotImplementedError(action)
            else:
                messages.error(request, _('Please check the form.'))

        elif action == 'invite-host':
            if invitation_form.is_valid():
                invitation = invitation_form.save(commit=False)
                invitation.programme = programme
                invitation.created_by = request.user
                invitation.save()

                invitation.send(request)

                messages.success(request, _('The host was successfully invited.'))

                return redirect('programme_admin_detail_view', event.slug, programme_id)
            else:
                messages.error(request, _('Please check the form.'))

        elif action == 'add-freeform-host':
            if freeform_organizer_form.is_valid():
                freeform_organizer_form = freeform_organizer_form.save(commit=False)
                freeform_organizer_form.programme = programme
                freeform_organizer_form.save()

                messages.success(request, _('The freeform organizer was successfully added.'))

                return redirect('programme_admin_detail_view', event.slug, programme_id)
            else:
                messages.error(request, _('Please check the form.'))

        elif (
            action.startswith('remove-host:') or
            action.startswith('remove-freeform-host:') or
            action.startswith('cancel-invitation:')
        ):
            action, id_str = action.split(':', 1)

            try:
                id_int = int(id_str)
            except ValueError:
                messages.error(request, _('Invalid action.'))
            else:
                if action == 'remove-host':
                    programme_role = get_object_or_404(ProgrammeRole, id=id_int, programme=programme)
                    programme_role.delete()

                    programme.apply_state(deleted_programme_roles=[programme_role])

                    messages.success(request, _('The host was removed.'))
                elif action == 'cancel-invitation':
                    invitation = get_object_or_404(Invitation, id=id_int, programme=programme, state='valid')
                    invitation.state = 'revoked'
                    invitation.save()

                    programme.apply_state()

                    messages.success(request, _('The invitation was cancelled.'))
                elif action == 'remove-freeform-host':
                    freeform_organizer = get_object_or_404(FreeformOrganizer, id=id_int, programme=programme)
                    freeform_organizer.delete()

                    programme.apply_state()

                    messages.success(request, _('The host was removed.'))
                else:
                    raise NotImplementedError(action)

                return redirect('programme_admin_detail_view', event.slug, programme_id)
        else:
            messages.error(request, _('Invalid action.'))

    invitations = programme.invitation_set.filter(state='valid')
    feedback = programme.visible_feedback

    tabs = [
        Tab('programme-admin-programme-tab', _('Programme form'), active=True),
        Tab('programme-admin-programme-schedule-tab', _('Schedule information')),
        Tab('programme-admin-programme-internal-tab', _('Internal information')),
        Tab('programme-admin-programme-reservations-tab', _('Seat reservations')),
        Tab('programme-admin-programme-hosts-tab', _('Programme hosts'), notifications=invitations.count()),
        Tab('programme-admin-programme-feedback-tab', _('Feedback'), notifications=feedback.count()),
    ]

    previous_programme, next_programme = programme.get_previous_and_next_programme()

    vars.update(
        change_invitation_role_forms=change_invitation_role_forms,
        feedback=feedback,
        forms_per_host=forms_per_host,
        freeform_organizer_form=freeform_organizer_form,
        freeform_organizers=FreeformOrganizer.objects.filter(programme=programme),
        internal_form=internal_form,
        invitation_form=invitation_form,
        invitations=invitations,
        is_using_paikkala_form=is_using_paikkala_form,
        next_programme=next_programme,
        overlapping_programmes=programme.get_overlapping_programmes(),
        paikkala_program_form=paikkala_program_form,
        previous_programme=previous_programme,
        programme_form=programme_form,
        programme_roles=programme_roles,
        programme=programme,
        schedule_form=schedule_form,
        tabs=tabs,
    )

    return render(request, 'programme_admin_detail_view.pug', vars)


@programme_admin_required
@require_POST
def programme_admin_change_host_role_view(request, vars, event, programme_id, programme_role_id):
    programme = get_object_or_404(ProgrammeManagementProxy, id=int(programme_id), category__event=event)
    programme_role = ProgrammeRole.objects.get(id=int(programme_role_id), programme=programme)
    change_role_form = initialize_form(ChangeHostRoleForm, request, prefix='chr', event=event, instance=programme_role)
    forms = [change_role_form]

    SignupExtra = event.programme_event_meta.signup_extra_model
    if SignupExtra.supports_programme:
        SignupExtraForm = SignupExtra.get_programme_form_class()
        signup_extra = SignupExtra.for_event_and_person(event, request.user.person)
        signup_extra_form = initialize_form(SignupExtraForm, request,
            prefix='sex',
            instance=signup_extra
        )
        forms.append(signup_extra_form)
    else:
        signup_extra_form = None

    if all(form.is_valid() for form in forms):
        instance = change_role_form.save()

        if signup_extra_form:
            signup_extra = signup_extra_form.process(signup_extra)

        instance.programme.apply_state()

        messages.success(request, _('The role was changed.'))
    else:
        messages.error(request, _("Please check the form."))

    programme = change_role_form.instance.programme

    return redirect('programme_admin_detail_view', programme.event.slug, programme.pk)


@programme_admin_required
@require_POST
def programme_admin_change_invitation_role_view(request, vars, event, programme_id, invitation_id):
    programme = get_object_or_404(ProgrammeManagementProxy, id=int(programme_id), category__event=event)
    invitation = Invitation.objects.get(id=int(invitation_id), programme=programme)
    change_role_form = initialize_form(ChangeInvitationRoleForm, request, prefix='cir', event=event, instance=invitation)

    if change_role_form.is_valid():
        instance = change_role_form.save()
        instance.programme.apply_state()
        messages.success(request, _('The role was changed.'))
    else:
        messages.error(request, _("Please check the form."))

    programme = change_role_form.instance.programme

    return redirect('programme_admin_detail_view', programme.event.slug, programme.pk)
