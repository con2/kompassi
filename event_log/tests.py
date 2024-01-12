from django.test import TestCase

from core.models import Event

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
        event2, unused = Event.get_or_create_dummy(name="Dummy event 2")

        kwargs = dict(
            channel="callback",
            callback_code=f"{__name__}:notification_callback",
        )

        subscription_with_event_filter, unused = Subscription.get_or_create_dummy(event_filter=event, **kwargs)
        subscription_without_event_filter, unused = Subscription.get_or_create_dummy(event_filter=None, **kwargs)

        entry_type = subscription_with_event_filter.entry_type

        emit(entry_type, event=event)
        emit(entry_type, event=event2)

        assert len(notifications) == 3
