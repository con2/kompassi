from babel.dates import format_skeleton
from dateutil.tz import tzlocal
from django.template import Library

from kompassi.core.utils import get_current_locale

__all__ = ["skeletonfmt"]
register = Library()


@register.filter
def skeletonfmt(datetime=None, skeleton="yMEd", tz=None, locale=None):
    if tz is None:
        tz = tzlocal()

    if locale is None:
        locale = get_current_locale()

    datetime = datetime.astimezone(tz)

    return format_skeleton(skeleton, datetime, locale=locale)
