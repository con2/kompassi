from behave import given, when, then

from django.core import mail

from core.models import ONE_TIME_CODE_LENGTH
from programme.models import ProgrammeEventMeta, Programme


@given(u'there is an event that has the programme functionality enabled')
def create_event_with_programme(context):
    context.meta, unused = ProgrammeEventMeta.get_or_create_dummy()
    context.event = context.meta.event


@when(u'I create a new programme')
@given(u'there is a programme')
def create_new_programme(context):
    context.programme, unused = Programme.get_or_create_dummy()


@when(u'I send the edit code to the programme host')
@given(u'its edit code has been sent to the programme host')
def send_edit_codes(context):
    context.request = context.request_factory.get('/')
    context.programme.send_edit_codes(context.request)


@then(u'the programme host receives the edit code via e-mail')
@when(u'the programme host receives the edit code via e-mail')
def receive_edit_code(context):
    body = mail.outbox[0].body

    # should have used a regex
    idx = body.find('/token/') + len('/token/')
    context.code = body[idx:idx + ONE_TIME_CODE_LENGTH]


@when(u'clicks the link in the message')
def step_impl(context):
    programme = ProgrammeEditCode.get_programme_by_code(context.code)
    assert programme is context.programme


@then(u'they should see the self-service editing page for the email')
def step_impl(context):
    pass


@when(u'the programme host edits the details of the programme')
def step_impl(context):
    pass


@when(u'submits the changes to the programme')
def step_impl(context):
    pass


@then(u'the changes to the programme should have been saved')
def step_impl(context):
    pass
