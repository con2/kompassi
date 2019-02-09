# https://gist.github.com/vbabiy/5842073

import re
import json

from django.conf import settings

from rest_framework.parsers import JSONParser


first_cap_re = re.compile('(.)([A-Z][a-z]+)')
all_cap_re = re.compile('([a-z0-9])([A-Z])')


def camel_to_underscore(name):
    s1 = first_cap_re.sub(r'\1_\2', name)
    return all_cap_re.sub(r'\1_\2', s1).lower()


def underscoreize(data):
    if isinstance(data, dict):
        new_dict = {}
        for key, value in data.items():
            new_key = camel_to_underscore(key)
            new_dict[new_key] = underscoreize(value)
        return new_dict
    if isinstance(data, (list, tuple)):
        for i in range(len(data)):
            data[i] = underscoreize(data[i])
        return data
    return data


class CamelCaseJSONRenderer(JSONParser):
    def parse(self, stream, media_type=None, parser_context=None):
        parser_context = parser_context or {}
        encoding = parser_context.get('encoding', settings.DEFAULT_CHARSET)

        data = stream.read().decode(encoding)
        return underscoreize(json.loads(data))
