from random import randint

from django.utils.timezone import now

from nexmo.models import InboundMessage


def fake_inbound_message(sender, message):
    return InboundMessage.new_message(
        nexmo_message_id=f"{randint(0, 20000):04x}",
        message=message,
        sender=sender,
        concat_ref=None,
        concat_part=None,
        concat_total=None,
        nexmo_timestamp=now(),
    )
