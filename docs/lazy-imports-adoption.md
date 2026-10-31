# Adopting PEP 810 `lazy import` in Kompassi

Status as of 2026-10-28. Decision: wait until Zed and VS Code highlight the
`lazy` keyword, then convert the whole backend in one go.

## Tool support

| Tool | Status | Notes |
|---|---|---|
| Python 3.15 | Shipped | Kompassi already runs 3.15 (`requires-python = ">=3.15"`, Docker images on 3.15). |
| ruff 0.17.2 (pinned) | Full | Parses, formats and sorts `lazy` imports. TID254 enforces always/never-lazy module lists, TID255 flags a lazy import that is resolved at module load. TC001–TC003 suggest `lazy` instead of `TYPE_CHECKING` on 3.15. No auto-fix yet for rewriting existing `TYPE_CHECKING` blocks, no rule that hoists function-body imports. |
| pyright 1.1.414 (pinned) | Full, verified locally | Parses the syntax and type-resolves the names (hover, return and argument errors all work). No changelog entry; support is implicit. |
| basedpyright 1.40.2 | Full, verified locally | Same engine as pyright 1.1.414. |
| Pylance (VS Code) | Full since prerelease 2026.2.104 | Issue microsoft/pylance-release#7891 closed 2026-06-04. |
| VS Code syntax highlighting | Missing | Bundled MagicPython grammar does not scope `lazy` yet. MagicStack/MagicPython#276 opened 2026-10-21, no PR. |
| Zed syntax highlighting | Missing | Zed synced its Python 3.15 highlights on 2026-06-01 but left `lazy` out pending tree-sitter/tree-sitter-python#336, which is still open. Diagnostics and navigation via basedpyright work. |

Editors already give correct diagnostics, hover and go-to-definition. Only the
keyword colour is missing, and on Zed a localized tree-sitter parse error on the
import line is possible.

## What there is to convert

Counts exclude tests, migrations, `.venv` and `kompassi/zombies/`.

| Pattern | Count |
|---|---|
| Imports inside function bodies | 1287 in 312 files |
| Files with `if TYPE_CHECKING:` blocks | 51 |
| Tail imports (module-level import after code) | 0 |

The function-body imports are almost all circular-import breakers between
model packages (`core.models`, `labour.models`, `badges.models`,
`intra.models`, `access.models`) and views importing their sibling `forms`
module.

## Conversion rules

1. **Function-body import → module-level `lazy from … import …`.** PEP 810
   forbids `lazy` inside functions, classes and `try` blocks, so each import
   is hoisted to the top of the module. This is safe for a circular import as
   long as the name is only used inside function bodies. A use in a class body
   or at module level (a `ForeignKey(Event)`, a default argument, a module
   constant) reifies the import during load and brings the cycle back.
   Enable TID255 before starting; it catches this statically.
2. **`TYPE_CHECKING` block → `lazy` import, case by case.** A name used only
   in annotations of plain classes and functions never resolves at runtime
   under 3.15's deferred annotations, so the conversion is safe. Pydantic
   models evaluate field annotations at class creation, so a `lazy` import
   there resolves immediately and ruff does not see it because the annotation
   looks deferred. Keep `TYPE_CHECKING` in pydantic models (for example
   `involvement/models/profile.py`) unless the name only appears in method
   signatures.
3. **One function-body import sits inside a `try` block.** It stays as is.
4. **Tail imports.** None found, nothing to do.

## Runtime behaviour to accept

- A lazy import that fails moves the error from process startup to the first
  request that touches the name. Tests cover the import graph well enough that
  this is mainly a concern for rarely exercised code paths.
- Django's app registry is fully loaded by the time any view or model method
  runs, so deferring model imports is safe.
- Ruff's import sorter groups eager imports before lazy ones within each
  section, so the diff will reorder import blocks.

## Plan when the editors are ready

1. Add `TID255` (and optionally `TID254`) to `extend-select` in
   `pyproject.toml`.
2. Convert one Django app at a time: hoist function-body imports to module
   level with `lazy`, convert eligible `TYPE_CHECKING` blocks, run
   `prek run --files …` and the test suite as the gate.
3. Land the whole conversion in one pull request so the import style does not
   stay mixed.

## Sources

- [PEP 810](https://peps.python.org/pep-0810/)
- [What's new in Python 3.15](https://docs.python.org/3.15/whatsnew/3.15.html)
- [Ruff tracking issue for lazy imports](https://github.com/astral-sh/ruff/issues/21305)
- [Ruff PR: rule flagging eagerly evaluated lazy imports](https://github.com/astral-sh/ruff/pull/25016)
- [Pylance: Support lazy imports](https://github.com/microsoft/pylance-release/issues/7891)
- [MagicPython: highlight `lazy` soft keyword](https://github.com/MagicStack/MagicPython/issues/276)
- [tree-sitter-python PR #336](https://github.com/tree-sitter/tree-sitter-python/pull/336)
- [Zed PR #57562, Python 3.15 highlight sync](https://github.com/zed-industries/zed/pull/57562)
