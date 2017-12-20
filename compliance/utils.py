from collections import namedtuple
from functools import wraps


PIINode = namedtuple('PIINode', 'parent exclude')


pii_roots = dict()


def pii_root(exclude=[]):
    def _decorator(cls):
        assert cls not in pii_roots
        pii_roots[cls] = PIINode(
            parent=None,
            exclude=exclude,
        )
        return cls
    return _decorator


def get_pii_dump(obj):
    assert obj.__class__ in pii_roots



def pii_dump_to_markdown(pii_dump):
    raise NotImplemented()
