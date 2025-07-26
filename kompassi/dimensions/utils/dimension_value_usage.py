from pathlib import Path
from typing import ClassVar, Self

import pydantic
from django.db import connection

from kompassi.dimensions.models.universe import Universe


class DimensionValueUsage(pydantic.BaseModel):
    """
    If done one by one, this is very slow. So we do it in bulk for the entire Universe.
    """

    response_count: int = 0
    involvement_count: int = 0
    program_count: int = 0
    schedule_item_count: int = 0

    query: ClassVar[str] = (Path(__file__).parent / "sql" / "dimension_value_usage.sql").read_text()

    @classmethod
    def for_universe(cls, universe: Universe) -> dict[int, dict[int, Self]]:
        result: dict[int, dict[int, Self]] = {}

        with connection.cursor() as cursor:
            cursor.execute(cls.query, dict(universe_id=universe.id))

            for row in cursor.fetchall():
                d_id, dv_id, response_count, involvement_count, program_count, schedule_item_count = row
                if not response_count and not involvement_count and not program_count and not schedule_item_count:
                    continue

                result.setdefault(d_id, {})[dv_id] = cls(
                    response_count=response_count,
                    involvement_count=involvement_count,
                    program_count=program_count,
                    schedule_item_count=schedule_item_count,
                )

        return result
