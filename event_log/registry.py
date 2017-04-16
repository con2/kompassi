# encoding: utf-8

from .models import EntryTypeMetadata


entry_types = dict()


def register(name, **kwargs):
    entry_types[name] = EntryTypeMetadata(name=name, **kwargs)
    return entry_types[name]


def get(entry_type_name):
    return entry_types[entry_type_name]
