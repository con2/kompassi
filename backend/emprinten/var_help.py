import typing

import jinja2.compiler

from .models import FileVersion
from .renderer import _TemplateCompiler, files_to_vfs, find_main


def _parse_node(node: jinja2.compiler.nodes.Node, out: set[str]):
    # XXX: This misses variables from includes / imports.

    if (nodes := getattr(node, "nodes", None)) is not None:
        # Classic tree, such as Template or Output.
        for child in nodes:
            _parse_node(child, out)
    if (inner := getattr(node, "node", None)) is not None:
        # e.g. filter applied to variable reference
        _parse_node(inner, out)
    if (args := getattr(node, "args", None)) is not None:
        # e.g. variable references in macro args
        for child in args:
            _parse_node(child, out)
    if isinstance(node, jinja2.compiler.nodes.Getattr):
        if isinstance(node.node, jinja2.compiler.nodes.Name) and node.node.name == "row":
            # A variable reference to `row`.
            out.add(node.attr)
        else:
            # e.g. method call on variable reference
            _parse_node(node.node, out)


def _parse_vars(env: _TemplateCompiler, source: str | None, **kwargs) -> set[str]:
    if source is None or not source:
        return set()

    ast = env.parse(source, **kwargs)
    out = set()
    for node in ast.body:
        _parse_node(node, out)
    return out


def find_vars(files: typing.Iterable[FileVersion], file_name_template: str, title_template: str) -> set[str]:
    env = _TemplateCompiler(files_to_vfs(files), handle_errors=False)
    main = find_main(files)
    if main is None:
        return set()
    main_source = env.get_source(main.file.file_name)

    main_vars = _parse_vars(env, main_source, filename=main.file.file_name)
    file_name_vars = _parse_vars(env, file_name_template, name="file_name")
    title_vars = _parse_vars(env, title_template, name="title")

    out = set()
    out.update(main_vars)
    out.update(file_name_vars)
    out.update(title_vars)

    return out
