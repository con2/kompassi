from __future__ import annotations

import re
from asyncio import Future, ensure_future
from functools import cached_property
from pathlib import Path
from typing import TYPE_CHECKING, Any, ClassVar

import pydantic

from .enums import PaymentProvider

if TYPE_CHECKING:
    from psycopg import AsyncConnection

# Keep in sync with kompassi.core.models.contact_email_mixin.CONTACT_EMAIL_RE
# (not imported to keep the optimized server free of Django imports)
CONTACT_EMAIL_RE = re.compile(r"(?P<name>.+) <(?P<email>.+@.+\..+)>")


class Event(pydantic.BaseModel):
    id: int
    slug: str
    name: str

    # TODO consider multiple payment providers per event in the future
    provider_id: PaymentProvider

    # NOTE SUPPORTED_LANGUAGES
    terms_and_conditions_url_en: str
    terms_and_conditions_url_fi: str
    terms_and_conditions_url_sv: str

    paytrail_merchant: str
    paytrail_password: str

    organization_name: str
    contact_email: str
    organization_business_id: str

    cache: ClassVar[dict[str | int, Event]] = {}
    cache_refresh: ClassVar[Future[dict[str | int, Event]] | None] = None

    query: ClassVar[bytes] = (Path(__file__).parent / "sql" / "get_events.sql").read_bytes()

    @classmethod
    async def get(cls, db: AsyncConnection, slug: str) -> Event | None:
        if cls.cache is None or slug not in cls.cache:
            cls.cache = await cls._refresh_cache(db)

        return cls.cache.get(slug)

    @classmethod
    async def _refresh_cache(cls, db: AsyncConnection) -> dict[str | int, Event]:
        """
        Ensure only one refresh is running at a time.
        """
        if cls.cache_refresh is None:
            cls.cache_refresh = ensure_future(cls._do_refresh_cache(db))

        try:
            return await cls.cache_refresh
        finally:
            cls.cache_refresh = None

    @classmethod
    async def _do_refresh_cache(cls, db: AsyncConnection):
        """
        Actually refresh the cache.
        """
        async with db.cursor() as cursor:
            await cursor.execute(cls.query)

            cls.cache.clear()
            async for row in cursor:
                event = cls(**dict(zip(cls.model_fields, row, strict=True)))  # type: ignore
                cls.cache[event.slug] = cls.cache[event.id] = event

        return cls.cache

    def model_dump(self, *args, **kwargs) -> Any:
        raise NotImplementedError("contains secrets, please don't")

    @property
    def plain_contact_email(self) -> str:
        """
        contact_email is stored in the "Name Surname <email@example.com>" format.
        Return the plain email address only (or the raw value if it is not in that format).
        """
        if match := CONTACT_EMAIL_RE.match(self.contact_email):
            return match.group("email")
        return self.contact_email

    @cached_property
    def provider(self):
        from ..providers.null import NullProvider
        from ..providers.paytrail import PaytrailProvider

        match self.provider_id:
            case PaymentProvider.NONE:
                return NullProvider(self)
            case PaymentProvider.PAYTRAIL:
                return PaytrailProvider(self)
            case _:
                raise NotImplementedError(f"Unknown payment provider: {self.provider_id}")
