from django.core.exceptions import ObjectDoesNotExist
from django.utils.timezone import now


def event_meta_property(app_label):
    def _get(self):
        try:
            return getattr(self, f"{app_label}eventmeta")
        except ObjectDoesNotExist:
            return None

    return property(_get)


def alias_property(name):
    def _get(self):
        return getattr(self, name)

    def _set(self, value):
        setattr(self, name, value)

    def _del(self):
        delattr(self, name)

    return property(_get, _set, _del)


def time_bool_property(name):
    """
    Uses a DateTimeField to implement a boolean property that records when the value was first set
    to True. This is best illustrated by the following table of transitions:

    False -> False: Nothing happens
    False -> True:  Underlying attribute is set to the current time
    True  -> False: Underlying attribute is set to None
    True ->  True:  Nothing happens
    """

    def _get(self):
        return getattr(self, name) is not None

    def _set(self, value):
        if bool(getattr(self, name)) == bool(value):
            pass
        else:
            setattr(self, name, now() if value else None)

    return property(_get, _set)
