from __future__ import annotations

from hashlib import blake2b

from django.db import models


class MessageBody(models.Model):
    """
    Deduplicated store of rendered (sanitized HTML) message bodies. Reused across
    MessageRecipients whose rendered body happens to be byte-identical (eg. a message
    with no placeholders sent to many recipients, or a PER_PERSON message body that
    does not vary per recipient).
    """

    digest = models.CharField(max_length=128, unique=True)
    text = models.TextField()

    id: int
    pk: int

    @classmethod
    def get_or_create(cls, text: str) -> tuple[MessageBody, bool]:
        # The unique constraint on `digest` makes get_or_create atomic under concurrent
        # sends (it retries the get on IntegrityError), so no dedup race handling needed.
        digest = blake2b(text.encode("utf-8")).hexdigest()
        return cls.objects.get_or_create(digest=digest, defaults=dict(text=text))
