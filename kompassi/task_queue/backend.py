from dataclasses import dataclass

from django.apps import apps
from django.core import checks
from django.tasks import Task, TaskResult, TaskResultStatus
from django.tasks.backends.base import BaseTaskBackend
from django.tasks.backends.immediate import ImmediateBackend
from django.tasks.exceptions import InvalidTask
from django.tasks.signals import task_enqueued
from django.utils import timezone

from .models import QueuedTask


@dataclass(frozen=True, slots=True, kw_only=True)
class PostgresTask(Task):
    """
    max_attempts=1 keeps at-most-once semantics: a task that raises or whose worker
    dies is not run again. Only tasks that are idempotent should ask for more.
    """

    max_attempts: int = 1


class PostgresTaskBackend(BaseTaskBackend):
    task_class = PostgresTask
    supports_defer = True
    supports_priority = True

    def validate_task(self, task):
        super().validate_task(task)
        if getattr(task, "max_attempts", 1) < 1:
            raise InvalidTask("max_attempts must be at least 1.")

    def enqueue(self, task, args, kwargs):
        self.validate_task(task)

        task_result = TaskResult(
            task=task,
            id="",
            status=TaskResultStatus.READY,
            enqueued_at=None,
            started_at=None,
            last_attempted_at=None,
            finished_at=None,
            args=args,
            kwargs=kwargs,
            backend=self.alias,
            errors=[],
            worker_ids=[],
        )

        row = QueuedTask.objects.create(
            func_path=task.module_path,
            args=task_result.args,
            kwargs=task_result.kwargs,
            queue_name=task.queue_name,
            priority=task.priority,
            run_after=task.run_after,
            max_attempts=getattr(task, "max_attempts", 1),
        )

        object.__setattr__(task_result, "id", str(row.id))
        object.__setattr__(task_result, "enqueued_at", timezone.now())
        task_enqueued.send(type(self), task_result=task_result)

        return task_result

    def check(self, **kwargs):
        if not apps.is_installed("kompassi.task_queue"):
            yield checks.Error(
                "kompassi.task_queue must be in INSTALLED_APPS to use PostgresTaskBackend.",
                id="kompassi.task_queue.E001",
            )


class ImmediateTaskBackend(ImmediateBackend):
    """
    For tests and one-off scripts: runs tasks inline but accepts the same task
    options (max_attempts) as PostgresTaskBackend so task definitions validate
    under both.
    """

    task_class = PostgresTask
