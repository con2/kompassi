from django.http import HttpResponse
from django.views.decorators.http import require_POST

from kompassi.core.utils import initialize_form
from kompassi.event_log_v2.utils.emit import emit

from ..forms import FeedbackForm


@require_POST
def feedback_view(request):
    feedback_form = initialize_form(FeedbackForm, request)

    if feedback_form.is_valid():
        emit(
            "feedback.feedbackmessage.created",
            request=request,
            context=request.headers.get("referer", ""),  # otherwise context would invariably be the feedback view
            feedback_message=feedback_form.cleaned_data["feedback"],
        )

        return HttpResponse(status=201)
    else:
        return HttpResponse(status=400)
