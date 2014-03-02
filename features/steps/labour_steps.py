from behave import given, when, then

from labour.models import LabourEventMeta

@given(u'there is an event that is accepting applications')
def given_event_accepting_applications(context):
    context.labour_event_meta, unused = LabourEventMeta.get_or_create_dummy()
    context.event = context.labour_event_meta.event