from behave import given, when, then

from django.utils import timezone
from django.core import mail

from mailings.models import Message, PersonMessage
from labour.models import LabourEventMeta

@given(u'the event has a message that is to be sent to all applicants')
def message_to_be_sent_to_all_applicants(context):
    applicants_group, unused = LabourEventMeta.get_or_create_group(
        event=context.event,
        suffix='applicants',
    )

    context.message = Message.objects.create(
        event=context.event,
        app_label='labour',
        recipient_group=applicants_group,
        subject_template='Test message subject',
        body_template='Test message body',
    )

    context.message.send()


@given(u'the event has a message that is to be sent to all accepted workers')
def message_to_be_sent_to_all_accepted(context):
    accepted, unused = LabourEventMeta.get_or_create_group(
        event=context.event,
        suffix='accepted'
    )

    context.message = Message.objects.create(
        event=context.event,
        app_label='labour',
        recipient_group=accepted,
        subject_template='Test message subject',
        body_template='Test message body',
    )

    context.message.send()


@then(u'I should receive the message')
def receive_the_message(context):
    person_message = PersonMessage.objects.get(
        person=context.person,
        message=context.message,
    )

    assert len(mail.outbox) == 2 # one for the person himself, and one for the monitor
