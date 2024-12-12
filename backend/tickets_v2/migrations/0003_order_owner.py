from pathlib import Path

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0042_alter_event_slug_alter_organization_slug"),
        ("tickets_v2", "0002_paymentstamp_trigger"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        # add ZERO_PRICE (noop)
        migrations.AlterField(
            model_name="paymentstamp",
            name="type",
            field=models.SmallIntegerField(
                choices=[
                    (0, "ZERO_PRICE"),
                    (1, "CREATE_PAYMENT_REQUEST"),
                    (2, "CREATE_PAYMENT_RESPONSE"),
                    (3, "PAYMENT_REDIRECT"),
                    (4, "PAYMENT_CALLBACK"),
                ]
            ),
        ),
        migrations.RunSQL(
            sql=Path(__file__).with_name("0003_order_owner.sql").read_text(),
            reverse_sql="""
                drop table if exists tickets_v2_orderowner cascade;
                drop index tickets_v2_order_email_idx;
            """,
            state_operations=[
                migrations.CreateModel(
                    name="OrderOwner",
                    fields=[
                        (
                            "order_id",
                            models.UUIDField(
                                primary_key=True,
                                serialize=False,
                            ),
                        ),
                        (
                            "event",
                            models.ForeignKey(
                                on_delete=django.db.models.deletion.CASCADE,
                                related_name="+",
                                to="core.event",
                            ),
                        ),
                        (
                            "user",
                            models.ForeignKey(
                                on_delete=django.db.models.deletion.CASCADE,
                                related_name="+",
                                to=settings.AUTH_USER_MODEL,
                            ),
                        ),
                    ],
                ),
            ],
        ),
    ]
