create or replace function task_queue_notify_ready() returns trigger as $$
  begin
    perform pg_notify('task_queue', new.queue_name);
    return null;
  end;
$$ language plpgsql;

create or replace trigger notify_ready
after insert or update on task_queue_queuedtask
for each row
when (new.status = 'READY')
execute function task_queue_notify_ready();
