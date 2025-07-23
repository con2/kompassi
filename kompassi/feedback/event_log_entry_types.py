from kompassi.event_log_v2 import registry

registry.register(
    name="feedback.feedbackmessage.created",
    message="Feedback received from {actor}",
    email_body_template="feedback_message_created.eml",
    email_reply_to=lambda entry: (entry.actor.email,) if entry.actor else (),
)
