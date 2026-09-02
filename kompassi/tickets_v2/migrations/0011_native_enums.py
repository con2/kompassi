from pathlib import Path

from django.db import migrations

import kompassi.field_types
from kompassi.tickets_v2.optimized_server.models import enums

REVERSE_SQL = """
-- Undo 0011_native_enums.sql: go back to smallint columns backed by domains.

create domain tickets_v2_paymentprovider_old as smallint constraint value_check check (value >= 0 and value <= 2);
create domain tickets_v2_paymentstamptype_old as smallint constraint value_check check (value >= 0 and value <= 11);
create domain tickets_v2_paymentstatus_old as smallint constraint value_check check (value >= 0 and value <= 7);
create domain tickets_v2_receipttype_old as smallint constraint value_check check (value in (3, 4, 7));
create domain tickets_v2_receiptstatus_old as smallint constraint value_check check (value >= 0 and value <= 3);

-- Drop triggers whose WHEN clause references a column we are about to retype.
drop trigger trigger_90_create_receipt on tickets_v2_paymentstamp;
drop trigger notify_requested on tickets_v2_receipt;

alter table tickets_v2_ticketsv2eventmeta rename column provider to provider_id;
alter table tickets_v2_ticketsv2eventmeta alter column provider_id drop default;
alter table tickets_v2_ticketsv2eventmeta
  alter column provider_id type tickets_v2_paymentprovider_old
  using (
    case provider_id::text
      when 'NONE' then 0
      when 'PAYTRAIL' then 1
      when 'STRIPE' then 2
    end
  )::tickets_v2_paymentprovider_old;
alter table tickets_v2_ticketsv2eventmeta alter column provider_id set default 0;

alter table tickets_v2_receipt alter column status drop default;
alter table tickets_v2_receipt
  alter column status type tickets_v2_receiptstatus_old
  using (
    case status::text
      when 'REQUESTED' then 0
      when 'PROCESSING' then 1
      when 'FAILURE' then 2
      when 'SUCCESS' then 3
    end
  )::tickets_v2_receiptstatus_old;
alter table tickets_v2_receipt alter column status set default 0;

alter table tickets_v2_receipt
  alter column type type tickets_v2_receipttype_old
  using (
    case type::text
      when 'PAID' then 3
      when 'CANCELLED' then 4
      when 'REFUNDED' then 7
    end
  )::tickets_v2_receipttype_old;

alter table tickets_v2_paymentstamp rename column provider to provider_id;
alter table tickets_v2_paymentstamp
  alter column status type tickets_v2_paymentstatus_old
  using (
    case status::text
      when 'NOT_STARTED' then 0
      when 'PENDING' then 1
      when 'FAILED' then 2
      when 'PAID' then 3
      when 'CANCELLED' then 4
      when 'REFUND_REQUESTED' then 5
      when 'REFUND_FAILED' then 6
      when 'REFUNDED' then 7
    end
  )::tickets_v2_paymentstatus_old;

alter table tickets_v2_paymentstamp
  alter column type type tickets_v2_paymentstamptype_old
  using (
    case type::text
      when 'ZERO_PRICE' then 0
      when 'CREATE_PAYMENT_REQUEST' then 1
      when 'CREATE_PAYMENT_SUCCESS' then 2
      when 'CREATE_PAYMENT_FAILURE' then 3
      when 'PAYMENT_REDIRECT' then 4
      when 'PAYMENT_CALLBACK' then 5
      when 'CANCEL_WITHOUT_REFUND' then 6
      when 'CREATE_REFUND_REQUEST' then 7
      when 'CREATE_REFUND_SUCCESS' then 8
      when 'CREATE_REFUND_FAILURE' then 9
      when 'REFUND_CALLBACK' then 10
      when 'MANUAL_REFUND' then 11
    end
  )::tickets_v2_paymentstamptype_old;

alter table tickets_v2_paymentstamp
  alter column provider_id type tickets_v2_paymentprovider_old
  using (
    case provider_id::text
      when 'NONE' then 0
      when 'PAYTRAIL' then 1
      when 'STRIPE' then 2
    end
  )::tickets_v2_paymentprovider_old;

alter table tickets_v2_order alter column cached_status drop default;
alter table tickets_v2_order
  alter column cached_status type tickets_v2_paymentstatus_old
  using (
    case cached_status::text
      when 'NOT_STARTED' then 0
      when 'PENDING' then 1
      when 'FAILED' then 2
      when 'PAID' then 3
      when 'CANCELLED' then 4
      when 'REFUND_REQUESTED' then 5
      when 'REFUND_FAILED' then 6
      when 'REFUNDED' then 7
    end
  )::tickets_v2_paymentstatus_old;
alter table tickets_v2_order alter column cached_status set default 0;

drop type tickets_v2_paymentprovider;
drop type tickets_v2_paymentstamptype;
drop type tickets_v2_paymentstatus;
drop type tickets_v2_receipttype;
drop type tickets_v2_receiptstatus;

alter domain tickets_v2_paymentprovider_old rename to tickets_v2_paymentprovider;
alter domain tickets_v2_paymentstamptype_old rename to tickets_v2_paymentstamptype;
alter domain tickets_v2_paymentstatus_old rename to tickets_v2_paymentstatus;
alter domain tickets_v2_receipttype_old rename to tickets_v2_receipttype;
alter domain tickets_v2_receiptstatus_old rename to tickets_v2_receiptstatus;

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
    receipt_type smallint;
  begin
    if new.type = 8 then
      receipt_type := 7;
    elsif new.status = 3 then
      receipt_type := 3;
    elsif new.status = 7 then
      receipt_type := 7;
    elsif new.status = 4 then
      if exists (
        select 1
        from tickets_v2_paymentstamp ps
        where
          ps.event_id = new.event_id and
          ps.order_id = new.order_id and
          ps.status = 3
      ) then
        receipt_type := 4;
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
      0,
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

create trigger trigger_90_create_receipt
after insert on tickets_v2_paymentstamp
for each row
when (new.status in (3, 4, 7) or new.type = 8)
execute function tickets_v2_paymentstamp_create_receipt();

create or replace trigger notify_requested
after insert or update on tickets_v2_receipt
for each row
when (new.status = 0)
execute function tickets_v2_receipt_notify_requested();
"""


class Migration(migrations.Migration):
    dependencies = [  # noqa: RUF012
        ("tickets_v2", "0010_cancellation_receipts"),
    ]

    operations = [  # noqa: RUF012
        migrations.RunSQL(
            sql=Path(__file__).with_name("0011_native_enums.sql").read_text(),
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
                    name="provider_id",
                    field=kompassi.field_types.PostgresEnumField(
                        enum=enums.PaymentProvider,
                        db_type_name="tickets_v2_paymentprovider",
                        choices=[(p.name, p.name) for p in enums.PaymentProvider],
                    ),
                ),
                migrations.RenameField(
                    model_name="paymentstamp",
                    old_name="provider_id",
                    new_name="provider",
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
                    model_name="receipt",
                    name="type",
                    field=kompassi.field_types.PostgresEnumField(
                        enum=enums.ReceiptType,
                        db_type_name="tickets_v2_receipttype",
                        choices=[(t.name, t.name) for t in enums.ReceiptType],
                    ),
                ),
                migrations.AlterField(
                    model_name="receipt",
                    name="status",
                    field=kompassi.field_types.PostgresEnumField(
                        enum=enums.ReceiptStatus,
                        db_type_name="tickets_v2_receiptstatus",
                        choices=[(s.name, s.name) for s in enums.ReceiptStatus],
                    ),
                ),
                migrations.AlterField(
                    model_name="ticketsv2eventmeta",
                    name="provider_id",
                    field=kompassi.field_types.PostgresEnumField(
                        enum=enums.PaymentProvider,
                        db_type_name="tickets_v2_paymentprovider",
                        choices=[(p.name, p.name) for p in enums.PaymentProvider],
                        default=enums.PaymentProvider.NONE,
                        verbose_name="Payment provider",
                    ),
                ),
                migrations.RenameField(
                    model_name="ticketsv2eventmeta",
                    old_name="provider_id",
                    new_name="provider",
                ),
            ],
        ),
    ]
