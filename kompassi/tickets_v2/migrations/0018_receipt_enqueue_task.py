from pathlib import Path

from django.db import migrations

REVERSE_SQL = """
create or replace function tickets_v2_receipt_notify_requested() returns trigger as $$
  begin
    perform pg_notify('tickets_v2_receipt', cast(new.event_id as text));
    return null;
  end;
$$ language plpgsql;

alter table tickets_v2_receipt add column batch_id uuid;
"""


class Migration(migrations.Migration):
    dependencies = [  # noqa: RUF012
        ("tickets_v2", "0017_default_unpaid_order_cancellation_delay"),
        ("task_queue", "0002_notify_ready"),
    ]

    operations = [  # noqa: RUF012
        migrations.RunSQL(
            sql=Path(__file__).with_name("0018_receipt_enqueue_task.sql").read_text(),
            reverse_sql=REVERSE_SQL,
        ),
    ]
