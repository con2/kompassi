from django.http import JsonResponse

from ..models import Like
from ..helpers import programme_event_required


@programme_event_required
def programme_likes_view(request, event):
    if not request.user.is_authenticated():
        return JsonResponse([])
    else:
        pass  # TODO
