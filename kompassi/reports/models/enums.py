from __future__ import annotations

from enum import Enum

Value = int | float | str | None


# named funnily to avoid ColumnType clash in GraphQL
class TypeOfColumn(Enum):
    INT = "int"
    STRING = "string"
    PERCENTAGE = "percentage"
    DATETIME = "datetime"

    # NUMERIC(10,2) in SQL
    # decimal.Decimal in Python
    # string of "0.00" in JSON
    # formatted as "0,00 €" in frontend
    CURRENCY = "currency"


class TotalBy(Enum):
    NONE = "NONE"
    SUM = "SUM"
    AVERAGE = "AVERAGE"
