# https://gist.github.com/vbabiy/5842073

import re
from collections.abc import Mapping, Sequence

from rest_framework.renderers import JSONRenderer


def underscore_to_camel(match):
    return match.group()[0] + match.group()[2].upper()


def camelize(data):
    # str is also a Sequence
    if isinstance(data, str):
        return data
    elif isinstance(data, Mapping):
        new_dict = {}
        for key, value in data.items():
            new_key = re.sub(r"[a-z]_[a-z]", underscore_to_camel, key)
            new_dict[new_key] = camelize(value)
        return new_dict
    elif isinstance(data, Sequence):
        for i in range(len(data)):
            data[i] = camelize(data[i])
        return data
    else:
        return data


class CamelCaseJSONRenderer(JSONRenderer):
    def render(self, data, *args, **kwargs):
        return super().render(camelize(data), *args, **kwargs)
