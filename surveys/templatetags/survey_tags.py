from django.template import Library

import yaml


__all__ = ["to_yaml"]
register = Library()


@register.filter
def to_yaml(obj):
    return yaml.dump(obj, default_flow_style=False)
