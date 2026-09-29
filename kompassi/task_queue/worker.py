"""
usage: python manage.py worker [--once]

Runs django.tasks Tasks enqueued by PostgresTaskBackend. The worker wakes on the
`task_queue` NOTIFY channel and additionally polls every POLL_INTERVAL_SECONDS so
that a notification lost while the worker was down only delays work by one interval.

Several replicas may run at once: claiming uses FOR UPDATE SKIP LOCKED.
"""

from __future__ import annotations

import json
import logging
import signal
from datetime import timedelta
from pathlib import Path
from traceback import format_exception

from django.db import connection, transaction
from django.tasks import Task, TaskContext, TaskResult, TaskResultStatus
from django.tasks.base import TaskError
from django.tasks.signals import task_finished, task_started
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.utils.module_loading import import_string
from psycopg import connect

from kompassi.tickets_v2.optimized_server.utils.uuid7 import uuid7_to_datetime

from .models import QueuedTask

logger = logging.getLogger(__name__)

NOTIFY_CHANNEL = "task_queue"
POLL_INTERVAL_SECONDS = 30
STOP_CHECK_INTERVAL_SECONDS = 1
BATCH_SIZE = 10
LEASE = timedelta(minutes=30)
RETRY_BASE_DELAY = timedelta(seconds=30)

CLAIM_SQL = (Path(__file__).parent / "sql" / "claim_tasks.sql").read_text()
RECLAIM_SQL = (Path(__file__).parent / "sql" / "reclaim_stale_tasks.sql").read_text()

OUTCOME_FIELDS = ["status", "run_after", "finished_at", "lease_expires_at", "errors"]


class LeaseExpired(Exception):
    pass


def retry_delay(attempts: int) -> timedelta:
    return RETRY_BASE_DELAY * 2 ** (attempts - 1)


def make_error(exception: BaseException) -> dict:
    exception_type = type(exception)
    return dict(
        exception_class_path=f"{exception_type.__module__}.{exception_type.__qualname__}",
        traceback="".join(format_exception(exception)),
    )


class Worker:
    def __init__(self):
        self.worker_id = get_random_string(32)
        self.stop_requested = False

    def request_stop(self, signum, frame):
        logger.info("Stop requested, finishing the current task")
        self.stop_requested = True

    def run_forever(self):
        signal.signal(signal.SIGTERM, self.request_stop)
        signal.signal(signal.SIGINT, self.request_stop)

        with connect(**connection.get_connection_params(), autocommit=True) as listen_conn:
            listen_conn.execute(f"listen {NOTIFY_CHANNEL}")
            logger.info("Worker %s listening on %s", self.worker_id, NOTIFY_CHANNEL)

            while not self.stop_requested:
                self.run_until_empty()
                self.wait_for_notification(listen_conn)

        logger.info("Worker %s stopped", self.worker_id)

    def wait_for_notification(self, listen_conn):
        # Waiting in short slices lets a SIGTERM be honoured promptly.
        waited = 0
        while not self.stop_requested and waited < POLL_INTERVAL_SECONDS:
            notified = False
            for _ in listen_conn.notifies(timeout=STOP_CHECK_INTERVAL_SECONDS, stop_after=1):
                notified = True
            if notified:
                break
            waited += STOP_CHECK_INTERVAL_SECONDS

        # Notifications carry no payload we act on; a single wake-up covers them all.
        for _ in listen_conn.notifies(timeout=0):
            pass

    def run_until_empty(self):
        self.reclaim_stale()
        while not self.stop_requested and self.run_batch():
            pass

    def reclaim_stale(self):
        error = make_error(LeaseExpired("Lease expired before the worker reported an outcome"))
        with connection.cursor() as cursor:
            cursor.execute(RECLAIM_SQL, dict(error=json.dumps([error])))
            reclaimed = cursor.fetchall()

        for task_id, status in reclaimed:
            logger.warning("Task id=%s had an expired lease, now %s", task_id, status)

    def claim_batch(self) -> list[QueuedTask]:
        with transaction.atomic():
            return list(
                QueuedTask.objects.raw(
                    CLAIM_SQL,
                    dict(
                        lease=LEASE,
                        batch_size=BATCH_SIZE,
                    ),
                )
            )

    def release(self, rows: list[QueuedTask]):
        """
        Hands unstarted rows back to the queue on shutdown so they don't wait for
        the lease to expire.
        """
        for row in rows:
            row.status = TaskResultStatus.READY
            row.attempts -= 1
            row.lease_expires_at = None
            row.save(update_fields=["status", "attempts", "lease_expires_at"])

    def run_batch(self) -> bool:
        """
        Returns True if there may be more work to do.
        """
        rows = self.claim_batch()

        for index, row in enumerate(rows):
            if self.stop_requested:
                self.release(rows[index:])
                return False
            self.run_task(row)

        return len(rows) == BATCH_SIZE

    def run_task(self, row: QueuedTask):
        try:
            task = import_string(row.func_path)
            if not isinstance(task, Task):
                raise TypeError(f"{row.func_path} is not a Task")
        except (ImportError, AttributeError, TypeError) as e:
            logger.exception("Task id=%s path=%s cannot be loaded", row.id, row.func_path)
            self.record_failure(row, e, retry=False)
            return

        task_result = self.to_task_result(task, row)
        task_started.send(sender=type(self), task_result=task_result)

        try:
            if task.takes_context:
                task.call(TaskContext(task_result=task_result), *row.args, **row.kwargs)
            else:
                task.call(*row.args, **row.kwargs)
        except KeyboardInterrupt:
            raise
        except BaseException as e:
            if not connection.in_atomic_block:
                connection.close_if_unusable_or_obsolete()
            self.record_failure(row, e, retry=row.attempts < row.max_attempts)
            if row.status == TaskResultStatus.FAILED:
                object.__setattr__(task_result, "status", TaskResultStatus.FAILED)
                object.__setattr__(task_result, "finished_at", row.finished_at)
                task_finished.send(sender=type(self), task_result=task_result)
            else:
                logger.warning(
                    "Task id=%s path=%s failed on attempt %s/%s, retrying at %s",
                    row.id,
                    row.func_path,
                    row.attempts,
                    row.max_attempts,
                    row.run_after,
                    exc_info=e,
                )
        else:
            row.status = TaskResultStatus.SUCCESSFUL
            row.finished_at = timezone.now()
            row.lease_expires_at = None
            row.save(update_fields=OUTCOME_FIELDS)
            object.__setattr__(task_result, "status", TaskResultStatus.SUCCESSFUL)
            object.__setattr__(task_result, "finished_at", row.finished_at)
            task_finished.send(sender=type(self), task_result=task_result)

    def record_failure(self, row: QueuedTask, exception: BaseException, retry: bool):
        row.errors = [*row.errors, make_error(exception)]
        row.lease_expires_at = None
        if retry:
            row.status = TaskResultStatus.READY
            row.run_after = timezone.now() + retry_delay(row.attempts)
        else:
            row.status = TaskResultStatus.FAILED
            row.finished_at = timezone.now()
        row.save(update_fields=OUTCOME_FIELDS)

    def to_task_result(self, task: Task, row: QueuedTask) -> TaskResult:
        return TaskResult(
            task=task,
            id=str(row.id),
            status=TaskResultStatus(row.status),
            enqueued_at=uuid7_to_datetime(row.id),
            started_at=row.started_at,
            last_attempted_at=row.last_attempted_at,
            finished_at=row.finished_at,
            args=row.args,
            kwargs=row.kwargs,
            backend=task.backend,
            errors=[TaskError(**error) for error in row.errors],
            # TaskResult.attempts is len(worker_ids), which tasks rely on to know
            # whether this is their last try. Earlier workers are not recorded.
            worker_ids=[self.worker_id] * row.attempts,
        )
