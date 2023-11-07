from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.shortcuts import redirect


from core.helpers import person_required
from payments.models.checkout_payment import CheckoutPayment, CHECKOUT_PAYMENT_WALL_ORIGIN

from ..helpers import membership_required


@membership_required
@require_http_methods(["POST"])
def membership_pay_fee_view(request, membership):
    current_term_payment = membership.get_payment_for_term()

    if not (current_term_payment and current_term_payment.can_pay_checkout):
        messages.error(request, "Et voi juuri nyt maksaa jäsenmaksua Kompassin kautta.")
        return redirect("core_organization_view", membership.organization.slug)

    checkout_payment = CheckoutPayment.from_membership_fee_payment(current_term_payment)
    checkout_payment.save()

    result = checkout_payment.perform_create_payment_request(request)

    return redirect(result["href"])
