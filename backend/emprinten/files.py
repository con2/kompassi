import csv
import io
import json
import os
import re
import typing
from collections import OrderedDict

import jinja2
from jinja2 import Template

Lut = dict[str, dict[str, str]]


# noinspection PyPropertyDefinition
class Pathlike(typing.Protocol):
    def open(self, mode: str = "rb") -> io.BytesIO: ...

    @property
    def name(self) -> str: ...


def make_lut(file: Pathlike, encoding: str) -> Lut:
    if file.name.endswith(".csv"):
        return csv_lookup(file, encoding)
    if file.name.endswith(".json"):
        return json_lookup(file, encoding)

    lut_type = f"Unsupported Lut file type: {file.name}"
    raise ValueError(lut_type)


non_word_char = re.compile(r"\W+")


def make_name(name: str) -> str:
    """
    Create a name suitable for template context, converting unsuitable character sequences to underscores.
    Any prefix or suffix underscores are removed.
    Result is lowercased.

    >>> make_name("")
    ''
    >>> make_name("Foo: - Bar")
    'foo_bar'
    >>> make_name("Barb!!")
    'barb'
    """
    return non_word_char.sub("_", name).strip("_").lower()


def parse_header_names(cols: list[str]) -> list[str]:
    names = [make_name(col) for col in cols]
    if len(names) != len(cols):
        fields = "Conflicting field names in header"
        raise ValueError(fields)
    return names


def open_text_io(file: Pathlike, encoding: str = "utf-8") -> io.TextIOBase:
    return io.TextIOWrapper(file.open(), encoding=encoding)


def csv_lookup(filename: Pathlike, encoding: str) -> Lut:
    """
    Create a lookup table from specially formatted csv.

    id,header1,header2,...
    key,value1,value2,...
    ...

    Note: key is included in the entry dict with name defined by header.
    """
    r: Lut = {}
    with open_text_io(filename, encoding=encoding) as csvfile:
        dialect = csv.Sniffer().sniff(csvfile.read(1024))
        csvfile.seek(0)
        reader = csv.reader(csvfile, dialect)
        header = next(reader)
        header = parse_header_names(header)
        for row in reader:
            row_data = OrderedDict(zip(header, row, strict=False))
            key = row[0]
            r[key] = row_data
    return r


def json_lookup(filename: Pathlike, encoding: str) -> Lut:
    """
    Create a lookup table from specially formatted json.

    {
       "": ["header1", "header2", ...],
       "key": ["value1", "value2", ...],
       ...
    }

    Note: key is not included in the entry dict.
    """
    with open_text_io(filename, encoding=encoding) as file:
        data = json.load(file)

    header = parse_header_names(data.pop(""))
    return {k: OrderedDict(zip(header, v, strict=False)) for k, v in data.items()}


def read_csv(csv_io: typing.TextIO) -> list[dict[str, str | dict[str, typing.Any]]]:
    data = []
    dialect = csv.Sniffer().sniff(csv_io.readline())
    csv_io.seek(0)
    reader = csv.reader(csv_io, dialect)
    header = next(reader)
    header = parse_header_names(header)
    for row_index, row in enumerate(reader):
        row_data: dict[str, typing.Any] = OrderedDict(zip(header, row, strict=False))
        row_data.setdefault(
            "META",
            {
                "index": row_index,
                "index1": row_index + 1,
            },
        )
        data.append(row_data)
    return data


class NameFactory:
    non_word = re.compile(r"[/\\?*<>|\"\0]+")
    whitespace = re.compile(r"\s+")
    max_len = 255
    index_fmt = " (%d)"

    def __init__(self, tpl: Template | None = None, max_len: int | None = None) -> None:
        self._names: dict[str, int] = {}
        self._tpl: Template | None = tpl
        self.max_len = max_len or NameFactory.max_len

    def make(self, row: dict[str, typing.Any], ext: str = ".pdf", fallback: str = "", post_format: str = "{}") -> str:
        """
        Make a unique name.

        >>> NameFactory(max_len=1).make({}, fallback="abcde")
        'a.pdf'
        >>> NameFactory(max_len=5).make({}, fallback="abcde")
        'abcde.pdf'
        >>> NameFactory().make({}, fallback="a  b\\tc\\r\\n\\nd")
        'a b c d.pdf'
        >>> e = NameFactory()
        >>> e.make({}, fallback="a")
        'a.pdf'
        >>> e.make({}, fallback="ERROR-a")
        'ERROR-a.pdf'
        >>> e.make({}, fallback="a", post_format="ERROR-{}")
        'ERROR-a (1).pdf'

        >>> f = NameFactory(max_len=5)
        >>> f.make({}, fallback="abcde")
        'abcde.pdf'
        >>> f.make({}, fallback="abcde")
        'abcde (1).pdf'
        >>> f.make({}, fallback="abcdefgh")
        'abcde (2).pdf'
        >>> f.make({}, fallback="a")
        'a.pdf'
        >>> f.make({}, fallback="a")
        'a (1).pdf'
        """
        fallback = fallback.removesuffix(ext)
        formatted = self.sanitize(self._render(row, fallback))

        if not formatted:
            formatted = fallback

        formatted = post_format.format(formatted)
        clipped = formatted[: self.max_len]

        new_number = self._names.get(clipped, -1) + 1
        self._names[clipped] = new_number

        if new_number > 0:
            return clipped + self.index_fmt % new_number + ext
        return clipped + ext

    def _render(self, row: dict, fallback: str) -> str:
        try:
            return self._tpl.render(row) if self._tpl is not None else fallback
        except jinja2.exceptions.SecurityError:
            raise
        except (jinja2.exceptions.TemplateError, ValueError):
            return fallback

    @classmethod
    def sanitize(cls, value: str, illegal_replacement: str = " ") -> str:
        """
        >>> NameFactory.sanitize("foo/bar/baz.txt")
        'foo bar baz.txt'
        >>> NameFactory.sanitize("   ")
        ''
        >>> NameFactory.sanitize("Foo?.txt")
        'Foo.txt'
        >>> NameFactory.sanitize("Foo?? Bar.txt")
        'Foo Bar.txt'
        """
        if not value:
            # None, "", Undefined
            return ""

        v = cls.whitespace.sub(" ", cls.non_word.sub(illegal_replacement, value)).strip()
        root, ext = os.path.splitext(v)
        root = root.strip()
        if ext:
            return root + ext.strip()
        return root
