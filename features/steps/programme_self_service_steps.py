from behave import given, when, then

from django.core import mail

from core.models import ONE_TIME_CODE_LENGTH
from programme.models import ProgrammeEventMeta, Programme, ProgrammeRole, ProgrammeEditToken


@given(u'there is an event that has the programme functionality enabled')
def create_event_with_programme(context):
    context.meta, unused = ProgrammeEventMeta.get_or_create_dummy()
    context.event = context.meta.event


@when(u'I create a new programme')
@given(u'there is a programme')
def create_new_programme(context):
    context.programme, unused = Programme.get_or_create_dummy()
    ProgrammeRole.get_or_create_dummy()


@when(u'I send the edit code to the programme host')
@given(u'its edit code has been sent to the programme host')
def send_edit_codes(context):
    context.request = context.request_factory.get('/')
    context.request.user = context.anonymous_user
    context.programme.send_edit_codes(context.request)


@then(u'the programme host receives the edit code via e-mail')
@when(u'the programme host receives the edit code via e-mail')
def receive_edit_code(context):
    body = mail.outbox[0].body

    # should have used a regex
    idx = body.find('/token/') + len('/token/')
    code = body[idx:idx + ONE_TIME_CODE_LENGTH]

    token = ProgrammeEditToken.objects.get(code=code)
    assert token.programme.pk == context.programme.pk
