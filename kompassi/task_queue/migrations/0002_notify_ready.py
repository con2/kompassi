from pathlib import Path

from django.db import migrations

REVERSE_SQL = """
drop trigger if exists notify_ready on task_queue_queuedtask;
drop function if exists task_queue_notify_ready();
"""


class Migration(migrations.Migration):
    dependencies = [  # noqa: RUF012
        ("task_queue", "0001_initial"),
    ]

    operations = [  # noqa: RUF012
        migrations.RunSQL(
            sql=Path(__file__).with_name("0002_notify_ready.sql").read_text(),
            reverse_sql=REVERSE_SQL,
        ),
    ]
