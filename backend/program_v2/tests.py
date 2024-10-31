from datetime import UTC, datetime, timedelta

import pytest

from core.models.event import Event

from .filters import ProgramFilters
from .models.program import Program
from .models.schedule import ScheduleItem


@pytest.mark.django_db
def test_program_filters():
    event, _ = Event.get_or_create_dummy()

    t1 = datetime.now(UTC)
    updated_after_t1 = ProgramFilters.from_query_dict({"updated_after": [t1.isoformat()]})

    p1 = Program(event=event, title="Program 1")
    p1.save()

    s1 = ScheduleItem(program=p1, start_time=datetime.now(UTC), length=timedelta(hours=1)).with_generated_fields()
    s1.save()

    t2 = datetime.now(UTC)
    updated_after_t2 = ProgramFilters.from_query_dict({"updated_after": [t2.isoformat()]})

    assert updated_after_t1.filter_program(event.programs.all()).count() == 1
    assert updated_after_t2.filter_program(event.programs.all()).count() == 0

    assert updated_after_t1.filter_schedule_items(event.schedule_items.all()).count() == 1
    assert updated_after_t2.filter_schedule_items(event.schedule_items.all()).count() == 0
