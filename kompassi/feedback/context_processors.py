from kompassi.core.utils import initialize_form

from .forms import FeedbackForm


def feedback_context(request):
    feedback_form = initialize_form(FeedbackForm, request)
    return dict(feedback_form=feedback_form)
