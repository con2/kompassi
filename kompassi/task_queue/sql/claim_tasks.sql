-- One row at a time: a claimed row that waited behind slower tasks in a batch
-- could see its lease expire before it was even started.
update task_queue_queuedtask t
set
  status = 'RUNNING',
  attempts = t.attempts + 1,
  started_at = coalesce(t.started_at, now()),
  last_attempted_at = now(),
  lease_expires_at = now() + %(lease)s
where t.id in (
  select id
  from task_queue_queuedtask
  where
    status = 'READY'
    and (run_after is null or run_after <= now())
  order by priority desc, id
  limit 1
  for update skip locked
)
returning *;
