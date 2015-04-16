from behave import given, when, then


@given(u'I change my email address')
@given(u'I have not verified my email address')
@when(u'I have not verified my email address')
def step_impl(context):
    context.person.email = 'something.else@example.com'

    request = context.request_factory.get('/')
    request.user = context.anonymous_user

    context.person.setup_email_verification(request)
    assert not context.person.is_email_verified


@then(u'I should receive an email verification message')
def step_impl(context):
    from django.core import mail

    assert len(mail.outbox) == 1
    context.email_verification_message = mail.outbox[0]


@when(u'I click the link in the email verification message')
def step_impl(context):
    from core.models import ONE_TIME_CODE_LENGTH

    body = context.email_verification_message.body

    # should have used a regex
    idx = body.find('/verify/') + len('/verify/')
    code = body[idx:idx + ONE_TIME_CODE_LENGTH]

    context.person.verify_email(code)


@then(u'my email address should be verified')
def step_impl(context):
    assert context.person.is_email_verified
