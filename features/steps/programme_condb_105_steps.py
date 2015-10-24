from behave import when, then

from programme.models import Programme, ProgrammeRole


@when(u'I assign it a schedule slot')
def step_impl(context):
    assert False

@when(u'I publish it')
def step_impl(context):
    assert False

@when(u'I create another programme')
def create_another_programme(context):
    context.another_programme, unused = Programme.get_or_create_dummy(title=u'Another dummy programme')
    ProgrammeRole.get_or_create_dummy(programme=context.another_programme)

@when(u'I do not assign it a schedule slot')
def step_impl(context):
    assert False

@then(u'I should see the first programme in the schedule')
def step_impl(context):
    assert False

@then(u'I should not see the second programme in the schedule')
def step_impl(context):
    assert False

@then(u'I should see the second programme on the non-schedule programme page')
def step_impl(context):
    assert False

@then(u'I should not see the first programme on the non-schedule programme page')
def step_impl(context):
    assert False