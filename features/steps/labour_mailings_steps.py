from behave import given, when, then

from django.utils import timezone

from mailings.models import Message, PersonMessage
from labour.models import LabourEventMeta

@given(u'the event has a message that is to be sent to all applicants')
def step_impl(context):
    applicants_group, unused = LabourEventMeta.get_or_create_group(
        event=context.event,
        suffix='applicants',
    )

    context.message, unused = Message.objects.get_or_create(
        event=context.event,
        app_label='labour',
        recipient_group=applicants_group,
        subject_template='Test message subject',
        body_template='Test message body',
    )

@given(u'the event has a message that is to be sent to all accepted workers')
def step_impl(context):
    applicants_group, unused = LabourEventMeta.get_or_create_group(
        event=context.event,
        suffix='accepted'
    )

    context.message, unused = Message.objects.get_or_create(
        event=context.event,
        app_label='labour',
        recipient_group=applicants_group,
        subject_template='Test message subject',
        body_template='Test message body',
    )

@then(u'I should receive the message')
def step_impl(context):
    person_message = PersonMessage.objects.get(
        person=context.person,
        message=context.message,
    )