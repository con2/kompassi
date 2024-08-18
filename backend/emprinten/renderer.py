import collections.abc
import contextlib
import functools
import html
import os
import shutil
import tempfile
import typing
import urllib.request
import zipfile

import jinja2.nodes
import weasyprint
from django.http import FileResponse, HttpResponse, HttpResponseBase
from jinja2 import FunctionLoader
from jinja2.sandbox import SandboxedEnvironment

from . import filters, functions
from .files import Lut, NameFactory, make_lut, make_name
from .models import FileVersion, ProjectFile

DEBUG = False

FileWithData = tuple[str, dict[str, str | dict[str, typing.Any]] | None, bool]
DataRow = dict[str, str | dict[str, typing.Any]]
DataSet = list[DataRow]
Vfs = dict[str, FileVersion]

LOCAL_FILE_URI_PREFIX = "file:///"
RENDER_FAILURE_FILE_NAME_PATTERN = "ERROR-{}"


def html_header(title: str, lang: str = "fi") -> str:
    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
     <meta charset="utf-8">
     <title>{title}</title>
</head>\n"""


def html_footer() -> str:
    return "\n</html>\n"


def ls_r(path: str) -> None:
    for ent in os.scandir(path):
        print(ent.path)
        if ent.is_dir():
            ls_r(ent.path)


def files_to_vfs(files: typing.Iterable[FileVersion]) -> Vfs:
    return {file_version.file.file_name: file_version for file_version in files}


def find_main(files: typing.Iterable[FileVersion]) -> FileVersion | None:
    for file_version in files:
        if file_version.file.type == ProjectFile.Type.Main:
            return file_version
    return None


def find_lookup_tables(files: typing.Iterable[FileVersion]) -> dict[str, Lut]:
    return {
        make_name(os.path.splitext(file_version.file.file_name)[0]): make_lut(file_version.data, "utf-8")
        for file_version in files
        if file_version.file.type == ProjectFile.Type.CSV
    }


@contextlib.contextmanager
def make_temp_dir(*, keep: bool) -> collections.abc.Generator[str, None, None]:
    tmp_dir = tempfile.mkdtemp()
    try:
        yield tmp_dir
    finally:
        if not keep:
            shutil.rmtree(tmp_dir)


def render_pdf(
    files: typing.Iterable[FileVersion],
    filename_pattern: str | None,
    title_pattern: str,
    data: DataSet,
    *,
    return_archive: bool = False,
    handle_errors: bool = False,
) -> HttpResponseBase:
    main = find_main(files)
    if main is None:
        return HttpResponse("Main file not found", status=404)

    vfs = files_to_vfs(files)
    env = _TemplateCompiler(vfs, handle_errors)
    if DEBUG:
        print(vfs)

    if DEBUG:
        print(data)

    with make_temp_dir(keep=False) as tmpdir:
        # tmpdir contents in the end (S for single file output, A for archive/split output):
        # - src/
        #   - master.html (S)
        #   - 001.html (A)
        #   - 002.html ...
        # - result/
        #   - master.pdf (S)
        #   - 001.pdf (A)
        #   - 002.pdf ...
        # - result.zip (A)

        # Either result/master.pdf or result.zip is streamed out.
        # master.pdf (S) is renamed when streamed.
        # ???.pdf (A) are renamed when written into the zip.

        src_dir = os.path.join(tmpdir, "src")
        result_dir = os.path.join(tmpdir, "result")
        os.mkdir(src_dir)
        os.mkdir(result_dir)

        # Compile source templates into one or more html's into $tmpdir/src.
        sources: list[FileWithData] = env.compile(
            main.file.file_name, src_dir, data, title_pattern, split_output=return_archive
        )

        wp = _HtmlCompiler(vfs)
        results: list[FileWithData] = wp.compile(sources, result_dir)
        name_tpl = env.from_string(filename_pattern) if filename_pattern else None
        name_factory = NameFactory(name_tpl)

        if return_archive:
            z_name = os.path.join(tmpdir, "result.zip")
            with zipfile.ZipFile(z_name, "w") as z:
                for pdf_name, row, success in results:
                    post_format = "{}" if success else RENDER_FAILURE_FILE_NAME_PATTERN
                    arc_name = name_factory.make(
                        {"row": row},
                        fallback=os.path.basename(pdf_name),
                        post_format=post_format,
                    )
                    z.write(pdf_name, arcname=arc_name)
            if DEBUG:
                ls_r(tmpdir)
            # FileResponse closes the open file by itself.
            return FileResponse(open(z_name, "rb"), content_type="application/zip")  # noqa: SIM115

        if len(results) > 1:
            return HttpResponse(status=401)

        if results:
            pdf_name, row, success = results[0]
            post_format = "{}" if success else RENDER_FAILURE_FILE_NAME_PATTERN
            file_name = name_factory.make({"row": row}, fallback="result.pdf", post_format=post_format)
            # FileResponse closes the open file by itself.
            return FileResponse(
                open(pdf_name, "rb"),  # noqa: SIM115
                content_type="application/pdf",
                filename=file_name,
            )

        return HttpResponse(status=201)


T = typing.TypeVar("T", bound=collections.abc.Callable)


class _TemplateCompiler:
    SafeBuiltins = (
        "dict.items",
        "dict.keys",
        "dict.values",
    )

    @staticmethod
    def wrap_as_safe_call(fn: T) -> T:
        @functools.wraps(fn)
        def wrapped(*args, **kwargs):
            return fn(*args, **kwargs)

        wrapped.is_safe_to_call = True  # pyright: ignore reportAttributeAccessIssue
        return typing.cast(T, wrapped)

    class Environment(SandboxedEnvironment):
        def is_safe_callable(self, obj: typing.Any) -> bool:
            if isinstance(obj, jinja2.runtime.Macro):
                return True
            if (
                type(obj).__name__ == "builtin_function_or_method"
                and getattr(obj, "__qualname__", None) in _TemplateCompiler.SafeBuiltins
            ):
                return True
            return hasattr(obj, "is_safe_to_call") and obj.is_safe_to_call

    def __init__(self, vfs: Vfs, handle_errors: bool) -> None:
        self.vfs = vfs
        self.handle_errors = handle_errors

        env = self.Environment(
            autoescape=True,
            loader=FunctionLoader(self._do_lookup),
        )
        # Mark some default global functions as safe.
        for name in ("cycler", "dict", "joiner", "lipsum", "range"):
            fn = env.globals.get(name)
            if fn is not None:
                env.globals[name] = self.wrap_as_safe_call(fn)

        filters.add_all_to(env.filters)
        env.globals.update({k: self.wrap_as_safe_call(v) for k, v in functions.get().items()})

        self.env = env

    def from_string(self, s: str | None) -> jinja2.Template | None:
        if s is None:
            return None
        return self.env.from_string(s)

    def get_source(self, file_name: str) -> str:
        return self.env.loader.get_source(self.env, file_name)[0]  # pyright: ignore reportOptionalMemberAccess

    def parse(self, source: str, **kwargs) -> jinja2.nodes.Template:
        return self.env.parse(source, **kwargs)

    def compile(
        self, main_file_name: str, src_dir: str, data: DataSet, title_pattern: str, *, split_output: bool
    ) -> list[FileWithData]:
        lookups = find_lookup_tables(self.vfs.values())
        tpl = self.env.get_template(main_file_name)
        _title_pattern = self.env.from_string(title_pattern)

        sources: list[FileWithData] = []
        if split_output:
            for idx, row in enumerate(data, start=1):
                row_copy = dict(row)
                title = _title_pattern.render(row=row_copy)

                src_name = os.path.join(src_dir, f"{idx:03d}.html")

                with open(src_name, "w") as of:
                    of.write(html_header(title=title))
                    success = self._write_render_or_error(of, tpl, row_copy, idx, lookups)
                    of.write(html_footer())
                sources.append((src_name, row_copy, success))
        else:
            # Render title if we have any data, but supply the row only if it is singular.
            row_copy = dict(data[0]) if len(data) == 1 else None
            title = _title_pattern.render(row=row_copy) if data else ""

            src_name = os.path.join(src_dir, "master.html")

            success = True
            with open(src_name, "w") as of:
                of.write(html_header(title=title))
                for idx, row in enumerate(data, start=1):
                    success &= self._write_render_or_error(of, tpl, dict(row), idx, lookups)
                of.write(html_footer())
            sources.append((src_name, row_copy, success))
        return sources

    def _write_render_or_error(self, of, tpl: jinja2.Template, row: dict, idx: int, lookups: dict) -> bool:
        try:
            of.write(tpl.render(row=row, **lookups))
            return True
        except jinja2.exceptions.SecurityError:
            # Don't return security details to user.
            raise
        except (jinja2.exceptions.TemplateError, ValueError) as e:
            if self.handle_errors:
                of.write(f"<h1>ERROR on data line {idx}</h1><pre>")
                of.write(html.escape(e.args[0] if e.args else ""))
                of.write("</pre>")
                return False
            raise

    # See `jinja2.loaders.FunctionLoader.__init__` for function signature.
    def _do_lookup(
        self,
        name: str,
    ) -> tuple[str, str, typing.Callable[[], bool]] | None:
        the_file: FileVersion | None = self.vfs.get(name)
        if DEBUG:
            print("Template lookup", name, the_file)
        if the_file is None:
            return None
        if the_file.file.type not in (
            ProjectFile.Type.Main,
            ProjectFile.Type.HTML,
            ProjectFile.Type.CSS,
        ):
            return None
        with the_file.data.open("rt") as tpl_file:
            src = tpl_file.read()
        return src, name, lambda: True


class _HtmlCompiler:
    def __init__(self, vfs: Vfs) -> None:
        self.vfs = vfs
        self.stylesheets = self.find_stylesheets(vfs.values())

    @staticmethod
    def find_stylesheets(files: typing.Iterable[FileVersion]) -> list[FileVersion]:
        return [file_version for file_version in files if file_version.file.type == ProjectFile.Type.CSS]

    def compile(self, sources: list[FileWithData], result_dir: str) -> list[FileWithData]:
        parsed_sheets = [
            weasyprint.CSS(
                string=sheet_file.data.read(),
                base_url=LOCAL_FILE_URI_PREFIX,
                url_fetcher=self._do_lookup,
            )
            for sheet_file in self.stylesheets
        ]
        results: list[FileWithData] = []
        for source, row, template_success in sources:
            pdf_html = weasyprint.HTML(
                filename=source,
                base_url=LOCAL_FILE_URI_PREFIX,
                url_fetcher=self._do_lookup,
            )
            pdf = pdf_html.write_pdf(
                stylesheets=parsed_sheets,
            )
            # We don't give `target` parameter, so the function should return bytes.
            if pdf is None:
                raise RuntimeError("Unexpectedly None result")

            dst_base = os.path.splitext(os.path.basename(source))[0]
            dst_name = os.path.join(result_dir, dst_base + ".pdf")
            results.append((dst_name, row, template_success))
            with open(dst_name, "wb") as of:
                of.write(pdf)

        return results

    # See `weasyprint.urls.default_url_fetcher` for function signature.
    # Note: At least some exceptions are silently ignored by weasyprint.
    def _do_lookup(self, url: str, timeout: int = 10, ssl_context=None) -> dict:
        if url.startswith("data:"):
            director = urllib.request.OpenerDirector()
            director.add_handler(urllib.request.DataHandler())
            data_response = director.open(url)
            if data_response is None:
                restricted_url = "Invalid data URL"
                raise ValueError(restricted_url)
            return {
                "redirected_url": url,
                "mime_type": data_response.headers["content-type"],
                "string": data_response.file.read(),
            }

        file_url = url.removeprefix(LOCAL_FILE_URI_PREFIX)
        if file_url == url:
            restricted_url = "Invalid URL to look up for"
            raise ValueError(restricted_url)
        the_file: FileVersion | None = self.vfs.get(file_url)
        if DEBUG:
            print("Pdf lookup", url, the_file)
        if the_file is None:
            raise KeyError
        return {
            "file_obj": the_file.data.open("rb"),
            # Weasyprint requires this to avoid file not found exc with the original filename.
            "redirected_url": file_url,
        }
