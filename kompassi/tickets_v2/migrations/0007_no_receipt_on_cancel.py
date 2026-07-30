from pathlib import Path

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [  # noqa: RUF012
        ("tickets_v2", "0006_alter_ticketsv2eventmeta_contact_email"),
    ]

    operations = [  # noqa: RUF012
        migrations.RunSQL(
            sql=Path(__file__).with_name("0007_no_receipt_on_cancel.sql").read_text(),
            reverse_sql=migrations.RunSQL.noop,
        ),
    ]
