from __future__ import annotations

import logging

from django.conf import settings
from django.core.mail import EmailMultiAlternatives

from kompassi.celery_app import app

from .models.enums import MessageDispatch

logger = logging.getLogger(__name__)


@app.task(ignore_result=True)
def send_message(message_id: str, involvement_ids: list[int] | None = None):
    """
    Sends `message` to all currently matching recipients, or, if `involvement_ids` is
    given, only to the (already matching) involvements with those ids - used for
    incremental auto-send. MessageRecipient's uniqueness constraints make this
    idempotent: recipients who already have a MessageRecipient row for this message are
    skipped.
    """
    from .models.message import Message
    from .models.message_body import MessageBody
    from .models.message_recipient import MessageRecipient
    from .rendering import render_body, render_email_html, render_subject

    message = Message.objects.select_related("reply_to", "universe__scope__event").get(id=message_id)
    event = message.event
    meta = event.program_v2_event_meta
    if meta is None:
        raise ValueError(f"Event {event.slug} has no ProgramV2EventMeta")

    involvements = message.resolve_involvements().select_related("person", "program")
    if involvement_ids is not None:
        involvements = involvements.filter(id__in=involvement_ids)

    if message.dispatch == MessageDispatch.PER_INVOLVEMENT:
        units = [(involvement.person, involvement) for involvement in involvements]
    else:
        units_by_person = {}
        for involvement in involvements:
            units_by_person.setdefault(involvement.person_id, (involvement.person, involvement))
        units = list(units_by_person.values())

    reply_to_email = message.reply_to.email if message.reply_to else meta.plain_contact_email

    num_sent = 0
    for person, involvement in units:
        involvement_for_recipient = involvement if message.dispatch == MessageDispatch.PER_INVOLVEMENT else None

        if MessageRecipient.objects.filter(
            message=message, person=person, involvement=involvement_for_recipient
        ).exists():
            continue

        program = involvement.program if involvement else None
        subject = render_subject(message.subject, event=event, person=person, involvement=involvement, program=program)
        body_html, body_text = render_body(
            message.body, event=event, person=person, involvement=involvement, program=program
        )
        body, _ = MessageBody.get_or_create(body_html)

        if settings.DEBUG:
            print(f"--- Messages V2: sending {subject!r} to {person.name_and_email} ---")
            print(body_text)

        email = EmailMultiAlternatives(
            subject=subject,
            body=body_text,
            from_email=meta.cloaked_contact_email,
            to=[person.name_and_email],
            reply_to=[reply_to_email] if reply_to_email else None,
        )
        email.attach_alternative(render_email_html(body_html, event=event, subject=subject), "text/html")

        # Only record a MessageRecipient (which doubles as the idempotency guard) once the
        # send actually succeeds - otherwise a transient failure would permanently mark
        # the person as sent-to and they'd never be retried on a subsequent (re-)send.
        try:
            email.send(fail_silently=False)
        except Exception:
            logger.exception("Failed to send message %s to %s", message.id, person.email)
            continue

        MessageRecipient.objects.create(
            message=message,
            person=person,
            involvement=involvement_for_recipient,
            email=person.email,
            subject=subject,
            body=body,
            cached_dimensions=involvement.cached_dimensions if involvement else {},
        )
        num_sent += 1

    logger.info("Sent message %s to %s recipients", message.id, num_sent)


@app.task(ignore_result=True)
def send_matching_messages(involvement_id: int):
    """
    Called whenever an involvement is created or its dimensions/is_active change.
    Sends every active Message of the involvement's event whose recipient filters now
    match this involvement, incrementally (only to this involvement).
    """
    from kompassi.dimensions.filters import DimensionFilters
    from kompassi.involvement.models.involvement import Involvement

    from .models.enums import MessageState
    from .models.message import Message
    from .models.message_recipient import MessageRecipient
    from .models.recipient_filters import group_to_dimension_filters

    try:
        involvement = Involvement.objects.get(id=involvement_id)
    except Involvement.DoesNotExist:
        return

    if not involvement.is_active:
        return

    active_messages = [
        message
        for message in Message.objects.filter(universe=involvement.universe)
        if message.state == MessageState.ACTIVE
    ]

    for message in active_messages:
        already_matched_person = (
            message.dispatch == MessageDispatch.PER_PERSON
            and MessageRecipient.objects.filter(
                message=message,
                person=involvement.person,
            ).exists()
        )
        if already_matched_person:
            continue

        matches = False
        for group in message.recipient_filters:
            filters = group_to_dimension_filters(group)
            if DimensionFilters(filters=filters).filter(Involvement.objects.filter(id=involvement.id)).exists():
                matches = True
                break

        if matches:
            send_message.delay(str(message.id), involvement_ids=[involvement.id])
