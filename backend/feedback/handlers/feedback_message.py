from event_log.utils import INSTANCE, log_creations

from ..models import FeedbackMessage

log_creations(
    FeedbackMessage,
    feedback_message=INSTANCE,
    created_by=lambda feedback_message: feedback_message.author,
    context=lambda feedback_message: feedback_message.context,
)
