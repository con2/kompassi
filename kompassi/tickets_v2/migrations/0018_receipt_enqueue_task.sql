-- Replaces the pg_notify body: a REQUESTED receipt now enqueues a django.tasks
-- Task for the generic worker instead of waking the receipt-specific one.
-- Column list must stay in sync with kompassi.task_queue.models.QueuedTask.
create or replace function tickets_v2_receipt_notify_requested() returns trigger as $$
  begin
    insert into task_queue_queuedtask (
      id,
      func_path,
      args,
      kwargs,
      queue_name,
      priority,
      status,
      max_attempts,
      attempts,
      worker_ids,
      errors
    ) values (
      uuidv7(),
      'kompassi.tickets_v2.tasks.send_receipt',
      jsonb_build_array(new.event_id, cast(new.id as text)),
      '{}',
      'default',
      0,
      'READY',
      3,
      0,
      '[]',
      '[]'
    );
    return null;
  end;
$$ language plpgsql;
