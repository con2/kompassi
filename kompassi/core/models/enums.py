from __future__ import annotations

from enum import Enum


class ProgramRoleRetentionPolicy(Enum):
    """
    NOTE: Declaration order must match the PostgreSQL enum type core_programroleretentionpolicy
    (Postgres enums compare by declaration order).
    """

    # No field value (NULL) means the person has not made a conscious choice. For now, NULL
    # behaves like RETAIN at retention cleanup; eventually NULL will be treated as REMOVE.
    REMOVE = "REMOVE"
    RETAIN = "RETAIN"
