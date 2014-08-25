from behave import given, when, then

@given(u'the event has badge types')
def event_has_badge_types(context):
    from badges.models import Template
    Template.get_or_create_dummy()

@then(u'I should have a badge of the correct type')
@then(u'the programme host should have a badge of the correct type')
def should_have_badge(context):
    from badges.models import Badge
    Badge.objects.get()
