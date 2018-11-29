from django.http import HttpResponse
from django.views.decorators.http import require_POST

from ipware.ip import get_ip

from core.utils import initialize_form

from ..forms import FeedbackForm


@require_POST
def feedback_view(request):
    feedback_form = initialize_form(FeedbackForm, request)

    if feedback_form.is_valid():
        feedback = feedback_form.save(commit=False)

        if request.user.is_authenticated:
            feedback.author = request.user

        feedback.context = request.META.get('HTTP_REFERER', '')
        feedback.author_ip_address = get_ip(request) or ''
        feedback.save()

        return HttpResponse(status=201)
    else:
        return HttpResponse(status=400)
