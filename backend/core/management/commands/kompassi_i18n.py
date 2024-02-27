import io
import logging
import os
import re

from babel.messages import Catalog, mofile, pofile
from babel.messages.extract import extract, extract_javascript, extract_python
from django.apps import apps
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.encoding import force_str
from django.utils.translation import templatize
from pypugjs import Compiler, process

ACCEPTABLE_FILENAMES_RE = re.compile(r"^.*\.(js|py|pug|html)$", re.I)


def extract_template(fileobj, keywords, comment_tags, options):
    src = force_str(fileobj.read(), "utf8")
    if fileobj.name.endswith(".pug"):
        src = process(src, compiler=Compiler)
    src = templatize(src)
    if "gettext" in src:
        src = re.sub(r"\n\s+", "\n", src)  # Remove indentation
        return extract_python(io.BytesIO(src.encode("utf8")), keywords, comment_tags, options)
    return ()


def filtered_walk(root):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [
            dirname
            for dirname in dirnames
            if dirname not in ("node_modules", "bower_components", "migrations", "management")
        ]
        if "site-packages" in dirpath:
            continue
        yield (dirpath, dirnames, filenames)


def _get_langs(langs, auto_lang):
    langs = set(langs or ())
    if auto_lang:
        langs.update({lang[0] for lang in settings.LANGUAGES})
    if "en" in langs:  # Ignore `en` (as that's the source language)
        langs.remove("en")
    return langs


def _get_pot_path(app):
    pot_path = os.path.join(app.path, "locale", "django.pot")
    if not os.path.isdir(os.path.dirname(pot_path)):
        os.makedirs(os.path.dirname(pot_path))
    return pot_path


def _get_po_path(app, language):
    po_path = os.path.join(app.path, "locale", language, "LC_MESSAGES", "django.po")
    if not os.path.isdir(os.path.dirname(po_path)):
        os.makedirs(os.path.dirname(po_path))
    return po_path


class Command(BaseCommand):
    def add_arguments(self, parser):
        """
        :type parser: argparse.ArgumentParser
        """
        parser.add_argument("-l", "--lang", nargs="*", dest="lang", help="languages to consider for update mode")
        parser.add_argument("-a", "--auto-lang", dest="auto_lang", action="store_true", help="use LANGUAGES for `-l`")
        parser.add_argument(
            "-e", "--extract", dest="extract", action="store_true", help="extract messages from source?"
        )
        parser.add_argument("-u", "--update", dest="update", action="store_true", help="update .po files from .pots?")
        parser.add_argument("-c", "--compile", dest="compile", action="store_true", help="compile .po files to .mos?")

    def handle(self, extract, update, compile, lang=(), auto_lang=False, *args, **options):
        self.log = logging.getLogger("kompassi_i18n")
        if options["verbosity"] > 1:
            logging.basicConfig(level=logging.INFO)
        langs = _get_langs(lang, auto_lang)
        for app in apps.get_app_configs():
            self.process_app(app, extract=extract, update=update, compile=compile, langs=langs)

    def process_app(self, app, extract=False, update=False, compile=False, langs=()):
        """
        :type app: django.apps.config.AppConfig
        """
        template_catalog = None
        if extract:
            template_catalog = self._extract(app)

        if update:
            self._update(app, template_catalog, langs)

        if compile:
            self._compile(app)

    def _update(self, app, template_catalog, langs):
        if template_catalog is None:
            with open(_get_pot_path(app)) as infp:
                template_catalog = pofile.read_po(infp, charset="utf8")

        for lang in langs:
            po_path = _get_po_path(app, language=lang)
            if os.path.isfile(po_path):
                with open(po_path) as infp:
                    lang_catalog = pofile.read_po(infp, charset="utf8")
            else:
                lang_catalog = Catalog(locale=lang, charset="utf8")
            lang_catalog.update(template_catalog)
            if len(lang_catalog):
                with open(po_path, "wb") as outf:
                    pofile.write_po(
                        outf,
                        lang_catalog,
                        width=1000,
                        omit_header=True,
                        sort_output=True,
                    )
                    self.log.info("%s: updated %s", app.label, po_path)

    def _extract(self, app):
        catalog = Catalog(domain="django", charset="utf8")
        files = {}
        for dirpath, _dirnames, filenames in filtered_walk(app.path):
            for filename in filenames:
                filename = os.path.join(dirpath, filename)
                if ACCEPTABLE_FILENAMES_RE.match(filename):
                    rel_filename = filename[len(os.path.commonprefix((app.path, filename))) + 1 :].replace(os.sep, "/")
                    files[rel_filename] = filename
        self.log.info("%s: %d translatable files found", app.label, len(files))
        extractors = self.get_extractors()
        for rel_filename, filename in sorted(files.items()):
            extractor_tup = extractors.get(os.path.splitext(filename)[1])
            if not extractor_tup:
                self.log.warning("Not sure how to extract messages from %s", filename)
                continue
            extractor, options = extractor_tup

            with open(filename, "rb") as fp:
                for _lineno, message, comments, _context in extract(extractor, fp, options=options):
                    catalog.add(message, locations=[(rel_filename, 0)], auto_comments=comments)
        if len(catalog):
            pot_path = _get_pot_path(app)
            with open(pot_path, "wb") as outf:
                pofile.write_po(outf, catalog, width=1000, omit_header=True, sort_output=True)
                self.log.info("%s: %d messages in %s", app.label, len(catalog), pot_path)
        return catalog

    def get_extractors(self):
        return {
            ".py": (extract_python, {}),
            ".js": (extract_javascript, {}),
            ".pug": (extract_template, {}),
            ".html": (extract_template, {}),
        }

    def _compile(self, app):
        for dirpath, _dirnames, filenames in filtered_walk(os.path.join(app.path, "locale")):
            for filename in filenames:
                filename = os.path.join(dirpath, filename)
                print(filename)
                if filename.endswith(".po"):
                    with open(filename) as infp:
                        catalog = pofile.read_po(infp)
                    if not len(catalog):
                        continue
                    bio = io.BytesIO()
                    mofile.write_mo(bio, catalog)
                    mo_file = filename.replace(".po", ".mo")
                    with open(mo_file, "wb") as outfp:
                        outfp.write(bio.getvalue())
                    self.log.info("%s compiled to %s", filename, mo_file)
