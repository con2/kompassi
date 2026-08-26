from django.db import migrations

# ALTER TYPE ... ADD VALUE cannot run in the same transaction as a statement that
# uses the new label (see migration 0013), so this migration only adds the labels
# and nothing else. atomic = False lets each RunSQL commit on its own.


class Migration(migrations.Migration):
    atomic = False

    dependencies = [  # noqa: RUF012
        ("tickets_v2", "0011_native_enums"),
    ]

    operations = [  # noqa: RUF012
        # NOTE: `if not exists`, because atomic = False means a failure partway leaves this
        # migration unrecorded with some labels already committed. Without it, the retry
        # would die on "label already exists" and need manual intervention.
        migrations.RunSQL(
            sql=(
                "alter type tickets_v2_paymentstatus "
                "add value if not exists 'PAID_AFTER_CANCELLATION' before 'REFUND_REQUESTED';"
            ),
            reverse_sql=migrations.RunSQL.noop,
        ),
        migrations.RunSQL(
            sql="alter type tickets_v2_paymentstamptype add value if not exists 'MANUAL_FULFILMENT';",
            reverse_sql=migrations.RunSQL.noop,
        ),
    ]
