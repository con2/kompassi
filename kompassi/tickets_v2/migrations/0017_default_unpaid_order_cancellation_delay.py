from django.db import migrations

# 0014 originally added the column with default 0, meaning "use the legacy midnight-three-
# days-ago rule". That rule is gone and 0 now means "automatic cancellation disabled", so
# rows created under the old default would silently stop cancelling unpaid orders. 0014's
# default has been amended, which covers fresh databases; this covers the ones that already
# ran it. Nothing has set the field deliberately yet — it and the legacy rule ship together.
#
# NOTE: the value is spelled out rather than imported from models.meta. A migration must keep
# working when the code around it moves on, and importing a live constant would both break
# `migrate` if it is ever renamed and silently rewrite history if its value ever changes.
# Keep in sync with DEFAULT_UNPAID_ORDER_CANCELLATION_DELAY_MINUTES only in the sense that
# this is the value that constant had when this migration was written.
DEFAULT_DELAY_MINUTES = 5040  # 84 hours


def set_default_delay(apps, schema_editor):
    TicketsV2EventMeta = apps.get_model("tickets_v2", "TicketsV2EventMeta")
    TicketsV2EventMeta.objects.filter(unpaid_order_cancellation_delay_minutes=0).update(
        unpaid_order_cancellation_delay_minutes=DEFAULT_DELAY_MINUTES,
    )


class Migration(migrations.Migration):
    dependencies = [  # noqa: RUF012
        ("tickets_v2", "0016_ensure_tickets_diagnostics"),
    ]

    operations = [  # noqa: RUF012
        migrations.RunPython(
            set_default_delay,
            reverse_code=migrations.RunPython.noop,
            elidable=True,
        ),
    ]
