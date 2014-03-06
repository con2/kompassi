from behave import given, when, then


@given(u'I have forgotten my password')
def step_impl(context):
    context.person.user.set_password("can't remember this")
    context.person.user.save()


@when(u'request a password reset')
def step_impl(context):
    request = context.request_factory.get('/')
    request.user = context.anonymous_user

    context.person.setup_password_reset(request)


@then(u'I should receive a password reset message')
def step_impl(context):
    from django.core import mail
    assert len(mail.outbox) == 1

    context.password_reset_message = mail.outbox[0]


@when(u'I click the link in the password reset message')
def step_impl(context):
    from core.models import ONE_TIME_CODE_LENGTH

    body = context.password_reset_message.body

    # should have used a regex
    idx = body.find('/reset/') + len('/reset/')
    context.code = body[idx:idx + ONE_TIME_CODE_LENGTH]


@when(u'set up a new password')
def step_impl(context):
    context.person.reset_password(context.code, 'a new password I can remember')


@then(u'my password should have been changed')
def step_impl(context):
    from django.contrib.auth import authenticate
    assert authenticate(
        username=context.person.user.username,
        password='a new password I can remember'
    )