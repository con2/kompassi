from behave import given, when, then

from messages.models import Message

@given(u'the event has a message that is to be sent to all applicants')
def step_impl(context):
    assert False

@when(u'I sign up for the event')
def step_impl(context):
    assert False

@then(u'I should receive the message')
def step_impl(context):
    assert False

@given(u'the evetn has a message that is to be sent to all accepted workers')
def step_impl(context):
    assert False

@when(u'the workforce manager approves my application')
def step_impl(context):
    assert False
