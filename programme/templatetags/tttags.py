from django.template import Library

import bleach


__all__ = ['removetags']
register = Library()


@register.filter
def strip_html(input_html):
    return bleach.clean(input_html, strip=True)
