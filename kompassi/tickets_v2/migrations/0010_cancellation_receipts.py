from pathlib import Path

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("tickets_v2", "0009_ticketsv2eventmeta_cancellation_period_days_and_more"),
    ]

    operations = [
        migrations.RunSQL(
            sql=Path(__file__).with_name("0010_cancellation_receipts.sql").read_text(),
            reverse_sql=Path(__file__).with_name("0007_no_receipt_on_cancel.sql").read_text(),
        ),
    ]
