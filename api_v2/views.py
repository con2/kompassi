from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from oauth2_provider.views.generic import ProtectedResourceView

from core.models import Person


class MyselfResource(ProtectedResourceView):
    def get(self, request, *args, **kwargs):
        person = get_object_or_404(Person, user=request.user)
        return JsonResponse(person.as_dict())
