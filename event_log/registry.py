from .models import EntryTypeMetadata


entry_types = dict()


def register(name, **kwargs):
    entry_types[name] = EntryTypeMetadata(name=name, **kwargs)
    return entry_types[name]


# Pseudo entry type for invalid entry types
register('event_log.entrytype.invalid', message='Invalid entry type')


def get(entry_type_name):
    return entry_types.get(entry_type_name, entry_types['event_log.entrytype.invalid'])
