# encoding: utf-8

from __future__ import unicode_literals

import logging

from django.db import transaction
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages

from core.helpers import person_required
from core.utils import initialize_form

from ..forms import ProgrammeSelfServiceForm, get_sired_invitation_formset
from ..models import Programme, ProgrammeRole, Invitation, FreeformOrganizer


logger = logging.getLogger('kompassi')


@person_required
def programme_profile_detail_view(request, programme_id):
    programme_role_qs = ProgrammeRole.objects.filter(person=request.user.person, programme=int(programme_id))
    try:
        programme_role = get_object_or_404(programme_role_qs)
    except ProgrammeRole.MultipleObjectsReturned:
        programme_role = programme_role_qs.first()
        logger.warn('Multiple roles for same programme/person: %s', programme_role.programme)

    programme = programme_role.programme
    event = programme.category.event

    form = initialize_form(ProgrammeSelfServiceForm, request,
        instance=programme,
        event=event,
        readonly=not programme.host_can_edit,
    )

    sired_invitation_formset = get_sired_invitation_formset(request, programme_role)

    forms = [form, sired_invitation_formset]

    SignupExtra = event.programme_event_meta.signup_extra_model
    if SignupExtra.supports_programme:
        SignupExtraForm = SignupExtra.get_programme_form_class()
        signup_extra = SignupExtra.for_event_and_person(event, request.user.person)
        signup_extra_form = initialize_form(SignupExtraForm, request,
            instance=signup_extra,
            prefix='extra',
        )
        forms.append(signup_extra_form)
    else:
        signup_extra = None
        signup_extra_form = None

    if request.method == 'POST':
        if not programme.host_can_edit:
            messages.error(request, programme.host_cannot_edit_explanation)
            return redirect('programme_profile_detail_view', programme.id)

        elif all(the_form.is_valid() for the_form in forms):
            with transaction.atomic():
                form.save()

                if signup_extra_form:
                    signup_extra = signup_extra_form.process(signup_extra)

                for extra_invite in sired_invitation_formset.save(commit=False):
                    extra_invite.programme = programme
                    extra_invite.created_by = request.user
                    extra_invite.role = programme_role.role
                    extra_invite.sire = programme_role
                    extra_invite.save()
                    extra_invite.send(request)

            messages.success(request, 'The changes were saved.')
            return redirect('programme_profile_view')

        else:
            messages.error(request, 'Please check the form.')

    vars = dict(
        event=event,
        form=form,
        signup_extra_form=signup_extra_form,
        freeform_organizers=FreeformOrganizer.objects.filter(programme=programme),
        host_can_invite_more=programme_role.extra_invites_left > 0,
        invitations=Invitation.objects.filter(programme=programme, state='valid'),
        programme=programme,
        programme_role=programme_role,
        programme_roles=ProgrammeRole.objects.filter(programme=programme),
        sired_invitation_formset=sired_invitation_formset,
    )

    return render(request, 'programme_profile_detail_view.jade', vars)
