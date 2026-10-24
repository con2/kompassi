from __future__ import annotations

from typing import TYPE_CHECKING

from kompassi.graphql_api.language import DEFAULT_LANGUAGE
from kompassi.reports.models.report import Report

from .paikkala_reports import ReservationsByZone, ReservationStatus

if TYPE_CHECKING:
    from ..models.meta import ProgramV2EventMeta


def get_reports(meta: ProgramV2EventMeta, lang: str = DEFAULT_LANGUAGE) -> list[Report]:
    reports: list[Report] = []
    reports.extend(ReservationStatus.report(meta.event))
    reports.extend(
        ReservationsByZone.report(schedule_item, lang=lang)
        for schedule_item in meta.schedule_items.filter(
            cached_combined_dimensions__contains=dict(paikkala=[]),
        )
    )
    return reports
