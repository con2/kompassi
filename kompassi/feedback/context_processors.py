from .forms import FeedbackForm


def feedback_context(request):
    return dict(feedback_form=FeedbackForm())
