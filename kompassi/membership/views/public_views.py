from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse

from kompassi.core.helpers import person_required
from kompassi.core.models import Organization, Person
from kompassi.core.utils import initialize_form

from ..forms import ApplicationForm
from ..helpers import membership_organization_required
from ..models import Membership, Term


@membership_organization_required
@person_required
def membership_apply_view(request, organization):
    meta = organization.membership_organization_meta
    mandatory_information_missing = not (
        request.user.person
        and request.user.person.official_first_names
        and request.user.person.surname
        and request.user.person.muncipality
        and request.user.person.email
    )
    already_member = Membership.objects.filter(
        organization=organization,
        person=request.user.person,
    ).exists()

    can_apply = (not mandatory_information_missing) and (not already_member)

    form = initialize_form(ApplicationForm, request)

    try:
        current_term = meta.get_current_term()
    except Term.DoesNotExist:
        current_term = None

    if request.method == "POST":
        if already_member:
            messages.error(request, "Olet jo jäsen tai jäsenhakemuksesi on jo käsiteltävänä.")
        elif mandatory_information_missing:
            messages.error(request, "Profiilistasi puuttuu pakollisia tietoja.")
        elif not form.is_valid():
            messages.error(request, "Tarkista lomakkeen tiedot.")
        else:
            membership = form.save(commit=False)
            membership.organization = organization
            membership.person = request.user.person
            membership.state = "approval"
            membership.save()

            messages.success(
                request,
                "Kiitos jäsenyyshakemuksestasi! Yhdistyksen hallitus käsittelee hakemuksesi seuraavassa kokouksessaan.",
            )

        return redirect("core_organization_view", organization.slug)

    vars = dict(
        already_member=already_member,
        can_apply=can_apply,
        form=form,
        mandatory_information_missing=mandatory_information_missing,
        meta=meta,
        organization=organization,
        current_term=current_term,
    )

    return render(request, "membership_apply_view.pug", vars)


@person_required
def membership_profile_view(request):
    memberships = Membership.objects.filter(person=request.user.person)
    potential_organizations = Organization.objects.filter(
        membershiporganizationmeta__receiving_applications=True,
    ).exclude(
        memberships__person=request.user.person,
    )

    vars = dict(
        memberships=memberships,
        potential_organizations=potential_organizations,
    )

    return render(request, "membership_profile_view.pug", vars)


def membership_organization_box_context(request, organization):
    meta = organization.membership_organization_meta
    if not meta:
        return dict()

    if Person.is_user_person(request.user):
        membership = Membership.objects.filter(
            organization=organization,
            person=request.user.person,
        ).first()
        is_membership_admin = meta.is_user_admin(request.user)
        current_term_payment = membership.get_payment_for_term() if membership else None
    else:
        membership = None
        is_membership_admin = False
        current_term_payment = None

    return dict(
        can_apply=meta.receiving_applications and not membership,
        current_term_payment=current_term_payment,
        is_membership_admin=is_membership_admin,
        membership=membership,
    )


def membership_profile_menu_items(request):
    membership_profile_url = reverse("membership_profile_view")
    membership_profile_active = request.path.startswith(membership_profile_url)
    membership_profile_text = "Yhdistysten jäsenyydet"

    return [(membership_profile_active, membership_profile_url, membership_profile_text)]
