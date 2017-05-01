from django.test import TestCase

from core.models import Event
from surveys.models import EventSurvey, EventSurveyResult

from .models import Subscription
from .utils import emit


notifications = []


def notification_callback(subscription, entry):
    notifications.append((subscription, entry))


class EventFilterTestCase(TestCase):
    def setUp(self):
        global notifications
        notifications = []

    def test_event_filter(self):
        event, unused = Event.get_or_create_dummy()
        event2, unused = Event.get_or_create_dummy(name='Dummy event 2')

        kwargs = dict(
            channel='callback',
            callback_code=f'{__name__}:notification_callback',
        )

        subscription_with_event_filter, unused = Subscription.get_or_create_dummy(event_filter=event, **kwargs)
        subscription_without_event_filter, unused = Subscription.get_or_create_dummy(event_filter=None, **kwargs)

        entry_type = subscription_with_event_filter.entry_type

        emit(entry_type, event=event)
        emit(entry_type, event=event2)

        assert len(notifications) == 3


class EventSurveyFilterTestCase(TestCase):
    def setUp(self):
        global notifications
        notifications = []

    def test_event_survey_filter(self):
        survey, unused = EventSurvey.get_or_create_dummy(title='Dummy survey')
        survey2, unused = EventSurvey.get_or_create_dummy(title='Dummy survey 2')

        kwargs = dict(
            entry_type='surveys.eventsurveyresult.created',
            channel='callback',
            callback_code=f'{__name__}:notification_callback',
        )

        subscription_with_filter, unused = Subscription.get_or_create_dummy(event_survey_filter=survey, **kwargs)
        subscription_without_filter, unused = Subscription.get_or_create_dummy(event_survey_filter=None, **kwargs)

        EventSurveyResult(survey=survey, model=dict()).save()
        EventSurveyResult(survey=survey2, model=dict()).save()

        assert len(notifications) == 3

