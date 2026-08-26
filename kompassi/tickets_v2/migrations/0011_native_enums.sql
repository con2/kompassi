-- Convert the smallint/domain-backed enum columns of tickets_v2 to native
-- PostgreSQL enum types. Values become the labels themselves (eg. 'PAID'
-- instead of 3); ordering comes from declaration order below, which must
-- match the declaration order of the corresponding Python OrderedEnum.
--
-- New types are created under a _new suffix, columns are rewritten onto
-- them, then the old domains are dropped and the new types renamed into
-- the names the domains used to occupy.

create type tickets_v2_paymentprovider_new as enum ('NONE', 'PAYTRAIL', 'STRIPE');

create type tickets_v2_paymentstamptype_new as enum (
  'ZERO_PRICE',
  'CREATE_PAYMENT_REQUEST', 'CREATE_PAYMENT_SUCCESS', 'CREATE_PAYMENT_FAILURE',
  'PAYMENT_REDIRECT', 'PAYMENT_CALLBACK',
  'CANCEL_WITHOUT_REFUND',
  'CREATE_REFUND_REQUEST', 'CREATE_REFUND_SUCCESS', 'CREATE_REFUND_FAILURE',
  'REFUND_CALLBACK', 'MANUAL_REFUND'
);

create type tickets_v2_paymentstatus_new as enum (
  'NOT_STARTED', 'PENDING', 'FAILED', 'PAID',
  'CANCELLED',
  'REFUND_REQUESTED', 'REFUND_FAILED', 'REFUNDED'
);

create type tickets_v2_receipttype_new as enum ('PAID', 'CANCELLED', 'REFUNDED');

create type tickets_v2_receiptstatus_new as enum ('REQUESTED', 'PROCESSING', 'FAILURE', 'SUCCESS');

-- Triggers whose WHEN clause references a column we are about to retype must be
-- dropped first; Postgres refuses to ALTER COLUMN TYPE otherwise. Both are
-- re-created further down with their WHEN clauses translated to labels.
drop trigger trigger_90_create_receipt on tickets_v2_paymentstamp;
drop trigger notify_requested on tickets_v2_receipt;

-- tickets_v2_order.cached_status
alter table tickets_v2_order alter column cached_status drop default;
alter table tickets_v2_order
  alter column cached_status type tickets_v2_paymentstatus_new
  using (
    case cached_status
      when 0 then 'NOT_STARTED'
      when 1 then 'PENDING'
      when 2 then 'FAILED'
      when 3 then 'PAID'
      when 4 then 'CANCELLED'
      when 5 then 'REFUND_REQUESTED'
      when 6 then 'REFUND_FAILED'
      when 7 then 'REFUNDED'
    end
  )::tickets_v2_paymentstatus_new;
alter table tickets_v2_order alter column cached_status set default 'NOT_STARTED';

-- tickets_v2_paymentstamp.{provider_id, type, status}
alter table tickets_v2_paymentstamp
  alter column provider_id type tickets_v2_paymentprovider_new
  using (
    case provider_id
      when 0 then 'NONE'
      when 1 then 'PAYTRAIL'
      when 2 then 'STRIPE'
    end
  )::tickets_v2_paymentprovider_new;

alter table tickets_v2_paymentstamp
  alter column type type tickets_v2_paymentstamptype_new
  using (
    case type
      when 0 then 'ZERO_PRICE'
      when 1 then 'CREATE_PAYMENT_REQUEST'
      when 2 then 'CREATE_PAYMENT_SUCCESS'
      when 3 then 'CREATE_PAYMENT_FAILURE'
      when 4 then 'PAYMENT_REDIRECT'
      when 5 then 'PAYMENT_CALLBACK'
      when 6 then 'CANCEL_WITHOUT_REFUND'
      when 7 then 'CREATE_REFUND_REQUEST'
      when 8 then 'CREATE_REFUND_SUCCESS'
      when 9 then 'CREATE_REFUND_FAILURE'
      when 10 then 'REFUND_CALLBACK'
      when 11 then 'MANUAL_REFUND'
    end
  )::tickets_v2_paymentstamptype_new;

alter table tickets_v2_paymentstamp
  alter column status type tickets_v2_paymentstatus_new
  using (
    case status
      when 0 then 'NOT_STARTED'
      when 1 then 'PENDING'
      when 2 then 'FAILED'
      when 3 then 'PAID'
      when 4 then 'CANCELLED'
      when 5 then 'REFUND_REQUESTED'
      when 6 then 'REFUND_FAILED'
      when 7 then 'REFUNDED'
    end
  )::tickets_v2_paymentstatus_new;

alter table tickets_v2_paymentstamp rename column provider_id to provider;

-- tickets_v2_receipt.{type, status}
alter table tickets_v2_receipt
  alter column type type tickets_v2_receipttype_new
  using (
    case type
      when 3 then 'PAID'
      when 4 then 'CANCELLED'
      when 7 then 'REFUNDED'
    end
  )::tickets_v2_receipttype_new;

alter table tickets_v2_receipt alter column status drop default;
alter table tickets_v2_receipt
  alter column status type tickets_v2_receiptstatus_new
  using (
    case status
      when 0 then 'REQUESTED'
      when 1 then 'PROCESSING'
      when 2 then 'FAILURE'
      when 3 then 'SUCCESS'
    end
  )::tickets_v2_receiptstatus_new;
alter table tickets_v2_receipt alter column status set default 'REQUESTED';

-- tickets_v2_ticketsv2eventmeta.provider_id (plain smallint column, never a domain)
alter table tickets_v2_ticketsv2eventmeta alter column provider_id drop default;
alter table tickets_v2_ticketsv2eventmeta
  alter column provider_id type tickets_v2_paymentprovider_new
  using (
    case provider_id
      when 0 then 'NONE'
      when 1 then 'PAYTRAIL'
      when 2 then 'STRIPE'
    end
  )::tickets_v2_paymentprovider_new;
alter table tickets_v2_ticketsv2eventmeta alter column provider_id set default 'NONE';
alter table tickets_v2_ticketsv2eventmeta rename column provider_id to provider;

-- Retire the domains and give the new types their names.
drop domain tickets_v2_paymentprovider;
drop domain tickets_v2_paymentstamptype;
drop domain tickets_v2_paymentstatus;
drop domain tickets_v2_receipttype;
drop domain tickets_v2_receiptstatus;

alter type tickets_v2_paymentprovider_new rename to tickets_v2_paymentprovider;
alter type tickets_v2_paymentstamptype_new rename to tickets_v2_paymentstamptype;
alter type tickets_v2_paymentstatus_new rename to tickets_v2_paymentstatus;
alter type tickets_v2_receipttype_new rename to tickets_v2_receipttype;
alter type tickets_v2_receiptstatus_new rename to tickets_v2_receiptstatus;

-- Re-create the trigger functions using label comparisons instead of magic numbers.
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
      -- Only notify cancellations of orders that were actually paid; abandoned
      -- unpaid orders are auto-cancelled by cron and must stay silent.
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
      new.correlation_id, -- one receipt per correlation_id (dedupes refund success vs callback)
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

create trigger trigger_90_create_receipt
after insert on tickets_v2_paymentstamp
for each row
when (new.status in ('PAID', 'CANCELLED', 'REFUNDED') or new.type = 'CREATE_REFUND_SUCCESS')
execute function tickets_v2_paymentstamp_create_receipt();

create or replace trigger notify_requested
after insert or update on tickets_v2_receipt
for each row
when (new.status = 'REQUESTED')
execute function tickets_v2_receipt_notify_requested();
