# encoding: utf-8

from .models import EntryTypeMetadata


entry_types = dict()


def register(**kwargs):
    name = kwargs['name']
    entry_types[name] = EntryTypeMetadata(**kwargs)


def get(entry_type_name):
    return entry_types[entry_type_name]
