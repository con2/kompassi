from datetime import date

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from kompassi.core.tabs import Tab
from kompassi.core.utils import initialize_form
from kompassi.event_log_v2.utils.emit import emit

from ..forms import MemberForm, MembershipFeePaymentForm, MembershipForm
from ..helpers import membership_admin_required
from ..models import Membership, MembershipFeePayment


@membership_admin_required
@require_http_methods(["GET", "HEAD", "POST"])
def membership_admin_member_view(request, vars, organization, person_id):
    membership = get_object_or_404(Membership, organization=organization, person=int(person_id))
    read_only = membership.person.user is not None
    member_form = initialize_form(MemberForm, request, instance=membership.person, readonly=read_only, prefix="member")
    membership_form = initialize_form(MembershipForm, request, instance=membership, prefix="membership")

    forms = [membership_form] if read_only else [membership_form, member_form]

    membership_fee_payments = MembershipFeePayment.objects.filter(
        term__organization=organization, member=membership
    ).order_by("term__end_date")
    current_term = membership.meta.get_current_term()
    current_term_payment = membership.get_payment_for_term(current_term) if current_term else None

    if current_term_payment:
        initial = dict(payment_date=current_term_payment.payment_date or date.today())
        membership_fee_payment_form = initialize_form(
            MembershipFeePaymentForm, request, instance=current_term_payment, initial=initial
        )
    else:
        membership_fee_payment_form = None

    if request.method == "POST":
        action = request.POST["action"]

        if action in ["save-edit", "save-return"]:
            if all(form.is_valid() for form in forms):
                for form in forms:
                    form.save()

                membership.apply_state()

                messages.success(request, "Jäsenen tiedot tallennettiin.")

                if action == "save-return":
                    return redirect("membership_admin_members_view", organization.slug)
                else:
                    return redirect("membership_admin_member_view", organization.slug, membership.person.id)
            else:
                messages.error(request, "Tarkista lomakkeen tiedot.")
        elif action == "mark-paid":
            payment = membership_fee_payment_form.save(commit=False)
            payment.save()

            messages.success(request, "Jäsenmaksu päivitetty.")
            return redirect("membership_admin_member_view", organization.slug, membership.person.id)
        else:
            raise NotImplementedError(action)

    previous_membership, next_membership = membership.get_previous_and_next()

    tabs = [
        Tab("membership-admin-person-tab", "Jäsenen tiedot", active=True),
        Tab("membership-admin-state-tab", "Jäsenyyden tila"),
        # Tab('membership-admin-events-tab', 'Jäsenyyteen liittyvät tapahtumat'),
        Tab("membership-admin-payments-tab", "Jäsenmaksut"),
    ]

    emit("core.person.viewed", request=request, person=membership.person.pk)

    vars.update(
        current_term=current_term,
        member_form=member_form,
        member=membership.person,
        membership_fee_payment_form=membership_fee_payment_form,
        membership_fee_payments=membership_fee_payments,
        membership_form=membership_form,
        membership=membership,
        next_membership=next_membership,
        previous_membership=previous_membership,
        read_only=read_only,
        tabs=tabs,
    )

    membership.person.log_view(request)

    return render(request, "membership_admin_member_view.pug", vars)
