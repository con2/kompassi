from django import template

__author__ = 'jyrkila'

register = template.Library()


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key, None)
