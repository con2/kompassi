# encoding: utf-8

from __future__ import unicode_literals

from django.db import transaction
from django.contrib import messages
from django.forms.models import modelformset_factory
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import ugettext_lazy as _

from core.helpers import person_required
from core.utils import initialize_form, initialize_form_set, set_defaults

from ..forms import ProgrammeOfferForm, get_sired_invitation_formset
from ..helpers import programme_event_required
from ..models import Invitation, ProgrammeRole, FreeformOrganizer


@programme_event_required
@person_required
def programme_offer_view(request, event, num_extra_invites=5):
    meta = event.programme_event_meta

    if not meta.is_accepting_cold_offers:
        messages.error(request, _(
            'This event is not currently accepting offers via this site. Please contact '
            'the programme managers directly.'
        ))
        return redirect('core_event_view', event.slug)

    form = initialize_form(ProgrammeOfferForm, request,
        event=event,
        prefix='needs',
    )

    sired_invitation_formset = get_sired_invitation_formset(request, num_extra_invites=num_extra_invites)

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
        if all(the_form.is_valid() for the_form in forms):
            with transaction.atomic():
                programme = form.save(commit=False)
                programme.state = 'offered'
                programme.save()

                programme_role = ProgrammeRole(
                    person=request.user.person,
                    programme=programme,
                    role=meta.default_role,
                )
                programme_role.save()

                if signup_extra_form:
                    signup_extra = signup_extra_form.process(signup_extra)

                for extra_invite in sired_invitation_formset.save(commit=False):
                    extra_invite.programme = programme
                    extra_invite.created_by = request.user
                    extra_invite.role = programme_role.role
                    extra_invite.sire = programme_role
                    extra_invite.save()
                    extra_invite.send(request)

            programme.apply_state()

            messages.success(request, _(
                'Thank you for offering your programme. The programme managers will be in touch.'
            ))

            return redirect('programme_profile_detail_view', programme.pk)
        else:
            messages.error(request, _('Please check the form.'))

    vars = dict(
        form=form,
        freeform_organizers=FreeformOrganizer.objects.none(),
        host_may_invite_more=num_extra_invites > 0,
        invitations=Invitation.objects.none(),
        num_extra_invites=num_extra_invites,
        programme_roles=ProgrammeRole.objects.none(),
        signup_extra_form=signup_extra_form,
        sired_invitation_formset=sired_invitation_formset,
    )

    return render(request, 'programme_offer_view.jade', vars)
