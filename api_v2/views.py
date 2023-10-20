from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.base import View
from django.contrib import messages
from django.utils.translation import gettext_lazy as _

from oauth2_provider.views.generic import ReadWriteScopedResourceView
from oauth2_provider.views import AuthorizationView
from oauth2_provider.exceptions import FatalClientError
from oauthlib.oauth2 import OAuth2Error

from core.models import Person, Event


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
        if not request.user.person.is_email_verified:
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
