from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import gettext_lazy as _
from django.views.generic.base import View
from oauth2_provider.views import AuthorizationView
from oauth2_provider.views.generic import ReadWriteScopedResourceView

from kompassi.core.models import Event, Person


class MyselfResource(ReadWriteScopedResourceView):
    http_method_names = ["get", "head"]

    def get(self, request, *args, **kwargs):
        person = get_object_or_404(Person, user=request.user)
        return JsonResponse(person.as_dict())


class EventResource(View):
    http_method_names = ["get", "head"]

    def get(self, request, event_slug):
        event = get_object_or_404(Event, slug=event_slug)
        return JsonResponse(event.as_dict())


class CustomAuthorizationView(AuthorizationView):
    def get(self, request, *args, **kwargs):
        if settings.KOMPASSI_OIDC_EMAIL_VERIFICATION_REQUIRED and not request.user.person.is_email_verified:
            messages.error(
                request,
                _(
                    "You need to verify your e-mail address before logging in to other services. "
                    "Please verify your e-mail address below and then try logging in again "
                    "from the service that sent you here."
                ),
            )
            return redirect("core_email_verification_request_view")

        return super().get(request, *args, **kwargs)
