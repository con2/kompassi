from __future__ import annotations

import pydantic

from .enums import TotalBy, TypeOfColumn

Value = int | float | str | None


class Column(pydantic.BaseModel):
    slug: str
    title: dict[str, str] = pydantic.Field(default_factory=dict)
    type: TypeOfColumn
    total_by: TotalBy = TotalBy.SUM

    def total_aggregate(self, values: list[Value]) -> Value:
        """
        We want to render the total row differently (tfoot > th).
        Additionally, producing it in SQL is usually a mess (UNION ALL etc).
        So produce it in Python.
        """
        if self.total_by == TotalBy.NONE:
            return ""

        numeric_values: list[int | float] = [value for value in values if isinstance(value, (int, float))]

        if not numeric_values:
            return ""

        match self.total_by:
            case TotalBy.SUM:
                return sum(numeric_values)
            case TotalBy.AVERAGE:
                return sum(numeric_values) / len(numeric_values)
            case _:
                raise NotImplementedError(self.total_by)
