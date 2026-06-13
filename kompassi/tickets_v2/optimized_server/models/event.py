from __future__ import annotations

import re
from datetime import datetime
from functools import cached_property
from pathlib import Path
from typing import Any, ClassVar

import pydantic
from async_lru import alru_cache

from .enums import PaymentProvider

# Keep in sync with kompassi.core.models.contact_email_mixin.CONTACT_EMAIL_RE
# (not imported to keep the optimized server free of Django imports)
CONTACT_EMAIL_RE = re.compile(r"(?P<name>.+) <(?P<email>.+@.+\..+)>")

# The admin can change settings that affect eg. customer cancellation eligibility
# at any time, so the cache needs to expire on its own.
CACHE_TTL_SECONDS = 5 * 60


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

    query: ClassVar[bytes] = (Path(__file__).parent / "sql" / "get_events.sql").read_bytes()

    @classmethod
    async def get(cls, slug: str) -> Event | None:
        events = await cls._load_all()
        return events.get(slug)

    @staticmethod
    @alru_cache(maxsize=1, ttl=CACHE_TTL_SECONDS)
    async def _load_all() -> dict[str | int, Event]:
        """
        Load all events into a slug/id-keyed dict, cached for CACHE_TTL_SECONDS.

        alru_cache gives us both TTL expiry and single-flight within a worker process:
        when the entry is missing or expired, concurrent callers coalesce into one
        execution and the rest await its result (a cancelled waiter does not abort it).

        It takes no arguments on purpose: alru_cache keys on call arguments, and a
        per-request pooled connection would be a different object every call, so the
        cache would never hit. The loader owns its own pooled connection instead
        (which also keeps the refresh independent of any single request's lifecycle).

        The DB work lives in _do_load() so tests can stub it while still exercising
        the real caching/single-flight behaviour through this wrapper.
        """
        return await Event._do_load()

    @staticmethod
    async def _do_load() -> dict[str | int, Event]:
        from ..db import get_connection_pool

        cache: dict[str | int, Event] = {}
        async with get_connection_pool().connection() as conn, conn.cursor() as cursor:
            await cursor.execute(Event.query)
            async for row in cursor:
                event = Event(**dict(zip(Event.model_fields, row, strict=True)))  # type: ignore
                cache[event.slug] = cache[event.id] = event

        return cache

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
