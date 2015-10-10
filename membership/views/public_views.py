# encoding: utf-8

from django.shortcuts import render, redirect
from django.contrib import messages

from core.helpers import person_required
from core.utils import initialize_form

from ..helpers import membership_organization_required
from ..models import Membership
from ..forms import MembershipForm


def membership_profile_box_context(request):
    return dict()


@membership_organization_required
@person_required
def membership_apply_view(request, organization):
    mandatory_information_missing = not (
        request.user.person and
        request.user.person.first_name and
        request.user.person.surname and
        request.user.person.muncipality and
        request.user.person.email
    )
    already_member = Membership.objects.filter(
        organization=organization,
        person=request.user.person,
    ).exists()

    can_apply = (not mandatory_information_missing) and (not already_member)

    form = initialize_form(MembershipForm, request)

    if request.method == 'POST':
        if already_member:
            messages.error(request, u'Olet jo jäsen tai jäsenhakemuksesi on jo käsiteltävänä.')
        elif mandatory_information_missing:
            messages.error(request, u'Profiilistasi puuttuu pakollisia tietoja.')
        elif not form.is_valid():
            messages.error(request, u'Tarkista lomakkeen tiedot.')
        else:
            membership = form.save(commit=False)
            membership.organization = organization
            membership.person = request.user.person
            membership.state = 'approval'
            membership.save()

            messages.success(request,
                u'Kiitos jäsenyyshakemuksestasi! Yhdistyksen hallitus käsittelee '
                u'hakemuksesi seuraavassa kokouksessaan.'
            )

        return redirect('core_organization_view', organization.slug)

    vars = dict(
        form=form,
        organization=organization,
        meta=organization.membership_organization_meta,
        mandatory_information_missing=mandatory_information_missing,
        already_member=already_member,
        can_apply=can_apply,
    )

    return render(request, 'membership_apply_view.jade', vars)


def membership_profile_view(request):
    raise NotImplementedError()


def membership_organization_box_context(request, organization):
    return dict()
