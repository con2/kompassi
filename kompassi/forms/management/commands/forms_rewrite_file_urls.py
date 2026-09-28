import logging

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.models import TextField
from django.db.models.functions import Cast

from ...models.response import Response

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = (
        "Rewrite file upload URLs stored in form responses after the S3 endpoint or bucket changed. "
        "File upload fields store full object URLs, and a response is only valid while they point at "
        "the bucket the app is currently configured for. Dry run unless --apply is given."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "old_prefix",
            help="URL prefix to replace, e.g. https://minio.con2.fi/kompassidev/",
        )
        parser.add_argument(
            "--new-prefix",
            default=f"{settings.AWS_S3_ENDPOINT_URL}/{settings.AWS_STORAGE_BUCKET_NAME}/",
            help="Replacement prefix; defaults to the configured endpoint and bucket",
        )
        parser.add_argument("--apply", action="store_true")

    def handle(self, *args, old_prefix: str, new_prefix: str, apply: bool, **opts):
        if not old_prefix.endswith("/") or not new_prefix.endswith("/"):
            raise ValueError("prefixes must end with a slash")

        responses_changed = 0
        urls_changed = 0
        # JSONField lookups JSON-encode their argument, so match on the serialized text instead.
        candidates = Response.objects.annotate(form_data_text=Cast("form_data", TextField())).filter(
            form_data_text__contains=old_prefix
        )
        for response in candidates.iterator():
            form_data, count = rewrite(response.form_data, old_prefix, new_prefix)
            if count == 0:
                continue
            responses_changed += 1
            urls_changed += count
            if apply:
                response.form_data = form_data
                response.save(update_fields=["form_data"])

        self.stdout.write(
            f"{'rewrote' if apply else 'would rewrite'} {urls_changed} URL(s) in {responses_changed} response(s)"
        )


def rewrite(form_data: dict, old_prefix: str, new_prefix: str) -> tuple[dict, int]:
    """
    File upload fields hold a list of object URLs; a single string is handled too in case older
    responses stored one. Other values are left untouched.
    """
    count = 0
    result = {}
    for slug, value in form_data.items():
        if isinstance(value, str) and value.startswith(old_prefix):
            value = new_prefix + value.removeprefix(old_prefix)
            count += 1
        elif isinstance(value, list):
            rewritten = []
            for item in value:
                if isinstance(item, str) and item.startswith(old_prefix):
                    item = new_prefix + item.removeprefix(old_prefix)
                    count += 1
                rewritten.append(item)
            value = rewritten
        result[slug] = value
    return result, count
