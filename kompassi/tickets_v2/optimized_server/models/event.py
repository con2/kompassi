from __future__ import annotations

import re
from asyncio import Lock
from datetime import UTC, datetime, timedelta
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

    cancellation_period_days: int
    start_time: datetime | None

    cache: ClassVar[dict[str | int, Event]] = {}
    cache_refreshed_at: ClassVar[datetime | None] = None

    # Serializes cache refreshes within a single worker process (one event loop).
    # The optimized server handles hundreds of concurrent requests, so without this
    # an expired cache would let every in-flight request kick off its own refresh.
    cache_lock: ClassVar[Lock] = Lock()

    # The admin can change settings that affect eg. customer cancellation eligibility
    # at any time, so the cache needs to expire on its own.
    cache_ttl: ClassVar[timedelta] = timedelta(minutes=5)

    query: ClassVar[bytes] = (Path(__file__).parent / "sql" / "get_events.sql").read_bytes()

    @classmethod
    def _cache_is_fresh(cls) -> bool:
        return cls.cache_refreshed_at is not None and datetime.now(UTC) - cls.cache_refreshed_at < cls.cache_ttl

    @classmethod
    async def get(cls, db: AsyncConnection, slug: str) -> Event | None:
        if cls._cache_is_fresh() and slug in cls.cache:
            return cls.cache.get(slug)

        async with cls.cache_lock:
            # Another request may have refreshed the cache while we waited for the lock.
            # Re-check under the lock so only the first arrival actually hits the database;
            # the rest fall straight through to the fresh cache.
            if not (cls._cache_is_fresh() and slug in cls.cache):
                await cls._do_refresh_cache(db)

        return cls.cache.get(slug)

    @classmethod
    async def _do_refresh_cache(cls, db: AsyncConnection):
        """
        Actually refresh the cache.
        """
        cache: dict[str | int, Event] = {}
        async with db.cursor() as cursor:
            await cursor.execute(cls.query)

            async for row in cursor:
                event = cls(**dict(zip(cls.model_fields, row, strict=True)))  # type: ignore
                cache[event.slug] = cache[event.id] = event

        # Swap in the fully-built cache atomically so concurrent readers never observe
        # a half-populated dict mid-refresh.
        cls.cache = cache
        cls.cache_refreshed_at = datetime.now(UTC)

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
