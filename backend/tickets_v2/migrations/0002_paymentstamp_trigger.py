from pathlib import Path

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("tickets_v2", "0001_initial"),
    ]

    operations = [
        migrations.RunSQL(
            sql=Path(__file__).with_name("0002_paymentstamp_trigger.sql").read_text(),
            reverse_sql="""
                drop trigger if exists notify_paid on tickets_v2_paymentstamp;
                drop function if exists tickets_v2_paymentstamp_notify_paid();
            """,
        ),
    ]
