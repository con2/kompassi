from behave import given, when, then

from django.utils import timezone
from django.core import mail

from mailings.models import RecipientGroup, Message, PersonMessage
from labour.models import LabourEventMeta

@given(u'the event has a message that is to be sent to all applicants')
@when(u'a message is added that should be sent to all applicants')
def message_to_be_sent_to_all_applicants(context):
    applicants_group, unused = LabourEventMeta.get_or_create_group(
        event=context.event,
        suffix='applicants',
    )

    context.message = Message.objects.create(
        recipient=RecipientGroup.objects.get(group=applicants_group),
        subject_template='Test message subject',
        body_template='Test message body',
    )

    context.message.send()


@given(u'the event has a message that is to be sent to all accepted workers')
@when(u'a message is added that should be sent to all accepted workers')
def message_to_be_sent_to_all_accepted(context):
    accepted_group, unused = LabourEventMeta.get_or_create_group(
        event=context.event,
        suffix='accepted',
    )

    context.message = Message.objects.create(
        recipient=RecipientGroup.objects.get(group=accepted_group),
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

    assert len(mail.outbox) == 1


@given(u'the event has a message that is to be sent to all workers with finished shifts')
def step_impl(context):
    finished_group, unused = LabourEventMeta.get_or_create_group(
        event=context.event,
        suffix='finished',
    )

    context.message = Message.objects.create(
        recipient=RecipientGroup.objects.get(group=finished_group),
        subject_template='Test message subject',
        body_template='Test message body {{ signup.formatted_shifts }}',
    )

    context.message.send()


@then(u'the message should include my shifts')
def step_impl(context):
    assert 'VUOROT' in mail.outbox[0].body
