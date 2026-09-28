from datetime import timedelta

from django.db import models
from django.tasks import TaskResultStatus
from django.utils.timezone import now

from kompassi.core.utils.cleanup import register_cleanup
from kompassi.tickets_v2.optimized_server.utils.uuid7 import uuid7

FINISHED_ROW_RETENTION = timedelta(days=7)


@register_cleanup(
    lambda qs: qs.filter(
        status__in=[TaskResultStatus.SUCCESSFUL, TaskResultStatus.FAILED],
        finished_at__lt=now() - FINISHED_ROW_RETENTION,
    )
)
class QueuedTask(models.Model):
    """
    One row per enqueued django.tasks Task. Rows are inserted by
    PostgresTaskBackend.enqueue and by database triggers (see tickets_v2 receipts),
    so any column added here must also get a value in those triggers.
    """

    id = models.UUIDField(primary_key=True, default=uuid7, editable=False)

    func_path = models.TextField()
    args = models.JSONField(default=list, blank=True)
    kwargs = models.JSONField(default=dict, blank=True)

    queue_name = models.TextField(default="default")
    priority = models.SmallIntegerField(default=0)
    status = models.TextField(choices=TaskResultStatus.choices, default=TaskResultStatus.READY)

    max_attempts = models.IntegerField(default=1)
    attempts = models.IntegerField(default=0)

    run_after = models.DateTimeField(null=True, blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    last_attempted_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    lease_expires_at = models.DateTimeField(null=True, blank=True)

    worker_ids = models.JSONField(default=list, blank=True)
    errors = models.JSONField(default=list, blank=True)

    class Meta:
        indexes = [  # noqa: RUF012
            models.Index(
                fields=["-priority", "id"],
                condition=models.Q(status=TaskResultStatus.READY),
                name="task_queue_ready_idx",
            ),
            models.Index(
                fields=["lease_expires_at"],
                condition=models.Q(status=TaskResultStatus.RUNNING),
                name="task_queue_running_idx",
            ),
        ]

    def __str__(self):
        return f"{self.func_path} ({self.status})"
