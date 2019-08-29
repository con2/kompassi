from django.template import Library

import bleach

from core.utils import slugify as core_slugify


__all__ = ['removetags', 'slugify']
register = Library()


@register.filter
def strip_html(input_html):
    return bleach.clean(input_html, strip=True)


slugify = register.filter(core_slugify)
