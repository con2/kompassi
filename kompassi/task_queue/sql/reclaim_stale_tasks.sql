update task_queue_queuedtask
set
  status = case when attempts < max_attempts then 'READY' else 'FAILED' end,
  finished_at = case when attempts < max_attempts then null else now() end,
  lease_expires_at = null,
  errors = errors || %(error)s::jsonb
where
  status = 'RUNNING'
  and lease_expires_at < now()
returning id, status;
