import bleach
from django.template import Library

from kompassi.core.utils import slugify as core_slugify

__all__ = ["strip_html", "slugify"]
register = Library()


@register.filter
def strip_html(input_html):
    return bleach.clean(input_html, strip=True)


slugify = register.filter(core_slugify)
