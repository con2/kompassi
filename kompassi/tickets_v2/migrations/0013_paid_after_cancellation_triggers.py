from pathlib import Path

from django.db import migrations

import kompassi.field_types
from kompassi.tickets_v2.optimized_server.models import enums

REVERSE_SQL = """
drop function if exists tickets_v2_ensure_tickets(int, uuid);

create or replace function tickets_v2_paymentstamp_update_order() returns trigger as $$
  begin
    update
      tickets_v2_order
    set
      cached_status = new.status
    where
      event_id = new.event_id and
      id = new.order_id and
      cached_status < new.status;

    return null;
  end;
$$ language plpgsql;

create or replace function tickets_v2_paymentstamp_create_receipt() returns trigger as $$
  declare
    receipt_type tickets_v2_receipttype;
  begin
    if new.type = 'CREATE_REFUND_SUCCESS' then
      receipt_type := 'REFUNDED';
    elsif new.status = 'PAID' then
      receipt_type := 'PAID';
    elsif new.status = 'REFUNDED' then
      receipt_type := 'REFUNDED';
    elsif new.status = 'CANCELLED' then
      if exists (
        select 1
        from tickets_v2_paymentstamp ps
        where
          ps.event_id = new.event_id and
          ps.order_id = new.order_id and
          ps.status = 'PAID'
      ) then
        receipt_type := 'CANCELLED';
      else
        return null;
      end if;
    else
      return null;
    end if;

    insert into tickets_v2_receipt (
      event_id,
      id,
      order_id,
      correlation_id,
      type,
      status,
      email
    )
    select
      new.event_id,
      new.correlation_id,
      new.order_id,
      new.correlation_id,
      receipt_type,
      'REQUESTED',
      o.email
    from
      tickets_v2_order o
    where
      o.event_id = new.event_id and
      o.id = new.order_id
    on conflict (event_id, id) do nothing;

    return null;
  end;
$$ language plpgsql;
"""


class Migration(migrations.Migration):
    dependencies = [  # noqa: RUF012
        ("tickets_v2", "0012_paid_after_cancellation"),
    ]

    operations = [  # noqa: RUF012
        migrations.RunSQL(
            sql=Path(__file__).with_name("0013_paid_after_cancellation_triggers.sql").read_text(),
            reverse_sql=REVERSE_SQL,
            state_operations=[
                migrations.AlterField(
                    model_name="order",
                    name="cached_status",
                    field=kompassi.field_types.PostgresEnumField(
                        enum=enums.PaymentStatus,
                        db_type_name="tickets_v2_paymentstatus",
                        choices=[(status.name, status.name) for status in enums.PaymentStatus],
                        default=enums.PaymentStatus.NOT_STARTED,
                        help_text="Payment status of the order. Updated by a trigger on PaymentStamp.",
                    ),
                ),
                migrations.AlterField(
                    model_name="paymentstamp",
                    name="status",
                    field=kompassi.field_types.PostgresEnumField(
                        enum=enums.PaymentStatus,
                        db_type_name="tickets_v2_paymentstatus",
                        choices=[(status.name, status.name) for status in enums.PaymentStatus],
                    ),
                ),
                migrations.AlterField(
                    model_name="paymentstamp",
                    name="type",
                    field=kompassi.field_types.PostgresEnumField(
                        enum=enums.PaymentStampType,
                        db_type_name="tickets_v2_paymentstamptype",
                        choices=[(t.name, t.name) for t in enums.PaymentStampType],
                    ),
                ),
            ],
        ),
    ]
