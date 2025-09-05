from __future__ import annotations

from collections.abc import Iterable
from datetime import date as date_type
from itertools import groupby
from typing import Self

import pydantic
from django.utils import translation

from kompassi.core.models.event import Event
from kompassi.core.utils.time_utils import format_date as _format_date
from kompassi.core.utils.time_utils import format_datetime
from kompassi.graphql_api.language import DEFAULT_LANGUAGE
from kompassi.program_v2.models.schedule_item import ScheduleItem
from kompassi.reports.models.report import Column, Report, TypeOfColumn


def format_date(date: date_type, lang: str) -> str:
    with translation.override(lang):
        return _format_date(date)


class ReservationStatus(pydantic.BaseModel):
    schedule_item_title: str
    total_reserved: int
    total_remaining: int
    total_capacity: int

    @classmethod
    def for_event(cls, event: Event) -> list[tuple[date_type, list[Self]]]:
        result = []

        for date, schedule_items in groupby(
            ScheduleItem.objects.filter(
                program__event=event,
                cached_combined_dimensions__contains=dict(paikkala=[]),
            ).order_by("start_time"),
            key=lambda x: x.start_time.date(),
        ):
            rows = []
            for schedule_item in schedule_items:
                baikal = schedule_item.paikkala_program
                if baikal is None:
                    continue

                row = cls(
                    schedule_item_title=schedule_item.title,
                    total_reserved=0,
                    total_remaining=0,
                    total_capacity=0,
                )

                for zone in baikal.zones.all():
                    zone_reservation_status = zone.get_reservation_status(baikal)
                    row.total_reserved += zone_reservation_status.total_reserved
                    row.total_remaining += zone_reservation_status.total_remaining
                    row.total_capacity += zone_reservation_status.total_capacity

                rows.append(row)
            result.append((date, rows))
        return result

    def as_row(self):
        return [
            self.schedule_item_title,
            self.total_reserved,
            self.total_remaining,
            self.total_capacity,
        ]

    @classmethod
    def report(cls, event: Event) -> list[Report]:
        return [
            Report(
                slug=f"reservation_status_{date.isoformat()}",
                title=dict(
                    en=f"Seat reservation status ({format_date(date, 'en')})",
                    fi=f"Paikkalippujen tilanne ({format_date(date, 'fi')})",
                ),
                columns=[
                    Column(
                        slug="schedule_item_title",
                        title=dict(
                            en="Schedule item",
                            fi="Aikataulumerkintä",
                        ),
                        type=TypeOfColumn.STRING,
                    ),
                    Column(
                        slug="total_reserved",
                        title=dict(
                            en="Total reserved",
                            fi="Varattu",
                        ),
                        type=TypeOfColumn.INT,
                    ),
                    Column(
                        slug="total_remaining",
                        title=dict(
                            en="Total remaining",
                            fi="Jäljellä",
                        ),
                        type=TypeOfColumn.INT,
                    ),
                    Column(
                        slug="total_capacity",
                        title=dict(
                            en="Total capacity",
                            fi="Kapasiteetti",
                        ),
                        type=TypeOfColumn.INT,
                    ),
                ],
                rows=[row.as_row() for row in rows],
            )
            for (date, rows) in cls.for_event(event)
        ]


class ReservationsByZone(pydantic.BaseModel):
    zone_name: str
    total_reserved: int
    total_remaining: int
    total_capacity: int

    @classmethod
    def for_schedule_item(cls, schedule_item: ScheduleItem) -> Iterable[Self]:
        baikal = schedule_item.paikkala_program
        if baikal is None:
            return

        for zone in baikal.zones.all():
            zone_reservation_status = zone.get_reservation_status(baikal)
            yield cls(
                zone_name=zone.name,
                total_reserved=zone_reservation_status.total_reserved,
                total_remaining=zone_reservation_status.total_remaining,
                total_capacity=zone_reservation_status.total_capacity,
            )

    def as_row(self):
        return [
            self.zone_name,
            self.total_reserved,
            self.total_remaining,
            self.total_capacity,
        ]

    @classmethod
    def report(
        cls,
        schedule_item: ScheduleItem,
        lang: str = DEFAULT_LANGUAGE,
    ) -> Report:
        room_sdv = schedule_item.dimensions.filter(value__dimension__slug="room").first()
        if room_sdv:
            room = f"{room_sdv.value.get_title(lang)} "
        else:
            room = ""

        with translation.override(lang):
            formatted_start_time = format_datetime(schedule_item.start_time)

        return Report(
            slug=f"reservations_by_zone_{schedule_item.slug}",
            title=dict(
                fi=f"Ohjelmanumeron paikkaliput: {schedule_item.title} ({room}{formatted_start_time})",
                en=f"Seat reservation status for program: {schedule_item.title} ({room}{formatted_start_time})",
            ),
            columns=[
                Column(
                    slug="zone_name",
                    title=dict(
                        en="Zone",
                        fi="Alue",
                    ),
                    type=TypeOfColumn.STRING,
                ),
                Column(
                    slug="total_reserved",
                    title=dict(
                        en="Total reserved",
                        fi="Varattu",
                    ),
                    type=TypeOfColumn.INT,
                ),
                Column(
                    slug="total_remaining",
                    title=dict(
                        en="Total remaining",
                        fi="Jäljellä",
                    ),
                    type=TypeOfColumn.INT,
                ),
                Column(
                    slug="total_capacity",
                    title=dict(
                        en="Total capacity",
                        fi="Kapasiteetti",
                    ),
                    type=TypeOfColumn.INT,
                ),
            ],
            has_total_row=True,
            rows=[row.as_row() for row in cls.for_schedule_item(schedule_item)],
        )
