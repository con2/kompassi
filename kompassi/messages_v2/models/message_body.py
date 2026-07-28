from __future__ import annotations

import logging
from hashlib import blake2b

from django.db import models

logger = logging.getLogger(__name__)


class MessageBody(models.Model):
    """
    Deduplicated store of rendered (sanitized HTML) message bodies. Reused across
    MessageRecipients whose rendered body happens to be byte-identical (eg. a message
    with no placeholders sent to many recipients, or a PER_PERSON message body that
    does not vary per recipient).
    """

    digest = models.CharField(max_length=128, db_index=True)
    text = models.TextField()

    id: int
    pk: int

    @classmethod
    def get_or_create(cls, text: str) -> tuple[MessageBody, bool]:
        digest = blake2b(text.encode("utf-8")).hexdigest()

        try:
            return cls.objects.get_or_create(digest=digest, defaults=dict(text=text))
        except cls.MultipleObjectsReturned:
            logger.warning("Multiple MessageBody returned for digest %s", digest)
            return cls.objects.filter(digest=digest, text=text).first(), False  # type: ignore
