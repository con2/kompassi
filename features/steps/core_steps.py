from behave import given, when, then

from core.models import Person


@given(u'I am a person')
@when(u'I register a new user account')
def given_i_am_a_person(context):
    context.person, unused = Person.get_or_create_dummy()


@when(u'I view the login page')
def step_impl(context):
    pass
