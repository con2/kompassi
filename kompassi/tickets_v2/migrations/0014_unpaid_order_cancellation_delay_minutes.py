from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [  # noqa: RUF012
        ("tickets_v2", "0013_paid_after_cancellation_triggers"),
    ]

    operations = [  # noqa: RUF012
        migrations.AddField(
            model_name="ticketsv2eventmeta",
            name="unpaid_order_cancellation_delay_minutes",
            field=models.PositiveIntegerField(
                default=0,
                help_text=(
                    "Number of minutes from order creation after which an unpaid order is "
                    "automatically cancelled. 0 = the legacy rule: unpaid orders done before "
                    "midnight three days ago are cancelled once a day."
                ),
            ),
        ),
    ]
