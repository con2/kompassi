import logging
from functools import wraps

from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404

from kompassi.tickets_v2.optimized_server.utils.paytrail_hmac import calculate_hmac

from .models import CheckoutPayment

logger = logging.getLogger(__name__)


def valid_signature_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        stamp = request.GET.get("checkout-stamp")
        if not stamp:
            logger.warning("Checkout: no checkout-stamp in query string params %r", request.GET)
            return HttpResponseBadRequest("no checkout-stamp")

        payment = get_object_or_404(CheckoutPayment, stamp=stamp)
        secret = payment.meta.checkout_password

        expected_signature = calculate_hmac(secret, request.GET)
        if request.GET.get("signature") != expected_signature:
            logger.warning("Checkout: invalid signature in query string params %r", request.GET)
            return HttpResponseBadRequest("invalid signature")

        # all is well and fun and games
        return view_func(request, payment, *args, **kwargs)

    return wrapper
