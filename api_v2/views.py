from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic.base import View

from oauth2_provider.views.generic import ReadWriteScopedResourceView

from core.models import Person, Event


class MyselfResource(ReadWriteScopedResourceView):
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        person = get_object_or_404(Person, user=request.user)
        return JsonResponse(person.as_dict())


class EventResource(View):
    http_method_names = ['get']

    def get(self, request, event_slug):
        event = get_object_or_404(Event, slug=event_slug)
        return JsonResponse(event.as_dict())
