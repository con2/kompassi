from datetime import timedelta

import pytest
from django.db import transaction
from django.tasks import TaskResultStatus, task
from django.test import override_settings
from django.utils import timezone

from kompassi.core.utils.cleanup import perform_cleanup

from .models import FINISHED_ROW_RETENTION, QueuedTask
from .worker import Worker, retry_delay

postgres_backend = override_settings(
    TASKS={"default": {"BACKEND": "kompassi.task_queue.backend.PostgresTaskBackend"}},
)

calls: list[tuple] = []


@task
def record_call(*args, **kwargs):
    calls.append((args, kwargs))


@task(max_attempts=3)
def flaky_task():
    calls.append(("flaky",))
    raise RuntimeError("boom")


@task
def failing_task():
    raise RuntimeError("boom")


@pytest.fixture(autouse=True)
def clear_calls():
    calls.clear()


@postgres_backend
@pytest.mark.django_db
def test_enqueue_is_transactional():
    # Enqueue writes a row on the caller's connection, so rolling back the
    # enclosing atomic block discards the task too.
    with transaction.atomic():
        record_call.enqueue(1)
        transaction.set_rollback(True)

    assert QueuedTask.objects.count() == 0

    with transaction.atomic():
        result = record_call.enqueue(1, key="value")

    row = QueuedTask.objects.get()
    assert str(row.id) == result.id
    assert row.status == TaskResultStatus.READY
    assert row.func_path == "kompassi.task_queue.tests.record_call"
    assert row.args == [1]
    assert row.kwargs == {"key": "value"}


@postgres_backend
@pytest.mark.django_db
def test_worker_runs_ready_tasks_and_skips_deferred():
    record_call.enqueue("now")
    record_call.using(run_after=timezone.now() + timedelta(hours=1)).enqueue("later")

    Worker().run_until_empty()

    assert calls == [(("now",), {})]
    assert QueuedTask.objects.get(args=["now"]).status == TaskResultStatus.SUCCESSFUL
    assert QueuedTask.objects.get(args=["later"]).status == TaskResultStatus.READY


@postgres_backend
@pytest.mark.django_db
def test_failure_without_retries_is_final():
    failing_task.enqueue()

    Worker().run_until_empty()

    row = QueuedTask.objects.get()
    assert row.status == TaskResultStatus.FAILED
    assert row.attempts == 1
    assert row.finished_at is not None
    assert row.errors[0]["exception_class_path"] == "builtins.RuntimeError"


@postgres_backend
@pytest.mark.django_db
def test_failure_with_retries_is_rescheduled_then_final():
    flaky_task.enqueue()
    worker = Worker()

    worker.run_until_empty()
    row = QueuedTask.objects.get()
    assert row.status == TaskResultStatus.READY
    assert row.attempts == 1
    assert row.run_after is not None
    assert row.run_after > timezone.now() + retry_delay(1) - timedelta(seconds=5)
    assert len(row.errors) == 1

    # The worker leaves it alone until run_after
    worker.run_until_empty()
    assert calls == [("flaky",)]

    # Postgres now() is frozen for the duration of the test transaction, so the
    # retry time must be moved clearly into the past rather than to "now".
    past = timezone.now() - timedelta(minutes=1)
    QueuedTask.objects.filter(id=row.id).update(run_after=past)
    worker.run_until_empty()
    QueuedTask.objects.filter(id=row.id).update(run_after=past)
    worker.run_until_empty()

    row.refresh_from_db()
    assert row.status == TaskResultStatus.FAILED
    assert row.attempts == 3
    assert len(row.errors) == 3
    assert calls == [("flaky",)] * 3


@postgres_backend
@pytest.mark.django_db
def test_stale_lease_is_reclaimed_according_to_max_attempts():
    retryable = record_call.enqueue("retryable")
    final = failing_task.enqueue()
    stale = timezone.now() - timedelta(minutes=1)
    QueuedTask.objects.filter(id=retryable.id).update(
        status=TaskResultStatus.RUNNING, attempts=1, max_attempts=2, lease_expires_at=stale
    )
    QueuedTask.objects.filter(id=final.id).update(status=TaskResultStatus.RUNNING, attempts=1, lease_expires_at=stale)

    Worker().reclaim_stale()

    assert QueuedTask.objects.get(id=retryable.id).status == TaskResultStatus.READY
    final_row = QueuedTask.objects.get(id=final.id)
    assert final_row.status == TaskResultStatus.FAILED
    assert "LeaseExpired" in final_row.errors[0]["exception_class_path"]


@postgres_backend
@pytest.mark.django_db
def test_outcome_of_a_reclaimed_task_is_discarded():
    record_call.enqueue("slow")
    worker = Worker()
    row = worker.claim()
    assert row is not None

    # Another worker found the lease expired and handed the row out again
    QueuedTask.objects.filter(id=row.id).update(lease_expires_at=timezone.now() + timedelta(hours=1), attempts=2)

    worker.run_task(row)

    fresh = QueuedTask.objects.get(id=row.id)
    assert fresh.status == TaskResultStatus.RUNNING
    assert fresh.attempts == 2
    assert fresh.finished_at is None


@postgres_backend
@pytest.mark.django_db
def test_unloadable_task_fails_without_retry():
    QueuedTask.objects.create(func_path="kompassi.task_queue.tests.no_such_task", max_attempts=3)

    Worker().run_until_empty()

    row = QueuedTask.objects.get()
    assert row.status == TaskResultStatus.FAILED


@postgres_backend
@pytest.mark.django_db
def test_nightly_cleanup_deletes_only_old_finished_rows():
    from kompassi.event_log_v2.models.entry import Entry

    Entry.ensure_partitions()

    old = timezone.now() - FINISHED_ROW_RETENTION - timedelta(days=1)
    recent = timezone.now() - timedelta(hours=1)
    keep = [
        QueuedTask.objects.create(func_path="x", status=TaskResultStatus.READY),
        QueuedTask.objects.create(func_path="x", status=TaskResultStatus.RUNNING, started_at=old),
        QueuedTask.objects.create(func_path="x", status=TaskResultStatus.SUCCESSFUL, finished_at=recent),
        QueuedTask.objects.create(func_path="x", status=TaskResultStatus.FAILED, finished_at=recent),
    ]
    QueuedTask.objects.create(func_path="x", status=TaskResultStatus.SUCCESSFUL, finished_at=old)
    QueuedTask.objects.create(func_path="x", status=TaskResultStatus.FAILED, finished_at=old)

    perform_cleanup()

    assert set(QueuedTask.objects.values_list("id", flat=True)) == {row.id for row in keep}
