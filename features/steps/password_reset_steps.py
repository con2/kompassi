from behave import given, when, then


@given(u'I have forgotten my password')
def step_impl(context):
    assert False


@when(u'request a password reset')
def step_impl(context):
    assert False


@then(u'I should receive a password reset message')
def step_impl(context):
    assert False


@when(u'I click the link in the password reset message')
def step_impl(context):
    assert False


@when(u'set up a new password')
def step_impl(context):
    assert False


@then(u'my password should have been changed')
def step_impl(context):
    assert False
