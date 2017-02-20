from event_log.utils import log_creations, INSTANCE

from ..models import FeedbackMessage


log_creations(
    FeedbackMessage,
    feedback_message=INSTANCE,
    created_by=lambda feedback_message: feedback_message.author
)
