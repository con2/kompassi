-- enums in kompassi.tickets_v2.optimized_server.models.enums
-- TODO should these be made proper postgres enums instead?
create domain tickets_v2_paymentprovider as smallint constraint value_check check (value >= 0 and value <= 2);
create domain tickets_v2_paymentstamptype as smallint constraint value_check check (value >= 0 and value <= 11);
create domain tickets_v2_paymentstatus as smallint constraint value_check check (value >= 0 and value <= 7);
create domain tickets_v2_receipttype as smallint constraint value_check check (value in (3, 4, 7));
create domain tickets_v2_receiptstatus as smallint constraint value_check check (value >= 0 and value <= 3);

create table tickets_v2_order (
  id uuid not null,
  event_id integer not null,
  order_number integer not null generated always as identity,
  owner_id integer,
  cached_status tickets_v2_paymentstatus not null default 0,
  cached_price numeric(10, 2) not null,
  language text not null,
  product_data jsonb not null,
  first_name text not null,
  last_name text not null,
  email text not null,
  phone text not null,

  primary key (event_id, id),
  foreign key (event_id) references core_event (id) deferrable initially deferred,
  foreign key (owner_id) references auth_user (id) deferrable initially deferred
) partition by list (event_id);

create index tickets_v2_order_id_idx on tickets_v2_order (id);
create index tickets_v2_order_owner_id_idx on tickets_v2_order (owner_id);
create index tickets_v2_order_cached_status_idx on tickets_v2_order (cached_status);
create index tickets_v2_order_email_idx on tickets_v2_order (email);


create table tickets_v2_ticket (
  id uuid not null,
  event_id integer not null,
  quota_id integer not null,
  order_id uuid,

  primary key (event_id, id),
  foreign key (event_id) references core_event (id),
  foreign key (event_id, order_id) references tickets_v2_order (event_id, id)
) partition by list (event_id);

create index tickets_v2_ticket_id_idx on tickets_v2_ticket (id);
create index tickets_v2_ticket_order_id_idx on tickets_v2_ticket (order_id) where order_id is not null;
create index tickets_v2_ticket_quota_id_idx on tickets_v2_ticket (quota_id) where order_id is null;


create table tickets_v2_paymentstamp (
  id uuid not null,
  event_id integer not null,
  order_id uuid not null,
  correlation_id uuid not null,
  provider_id tickets_v2_paymentprovider not null,
  type tickets_v2_paymentstamptype not null,
  status tickets_v2_paymentstatus not null,
  data jsonb not null default '{}',

  primary key (event_id, id),
  foreign key (event_id) references core_event (id),
  foreign key (event_id, order_id) references tickets_v2_order (event_id, id)
) partition by list (event_id);

create index tickets_v2_paymentstamp_id_idx on tickets_v2_paymentstamp (id);
create index tickets_v2_paymentstamp_order_id_idx on tickets_v2_paymentstamp (order_id);

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

create trigger trigger_00_update_order
after insert on tickets_v2_paymentstamp
for each row
execute function tickets_v2_paymentstamp_update_order();

-- Create a receipt only if this is the first time we see this payment
create or replace function tickets_v2_paymentstamp_create_receipt() returns trigger as $$
  begin
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
      new.correlation_id, -- this ensures that we only create one receipt per payment
      new.order_id,
      new.correlation_id,
      new.status, -- PaymentStatus.PAID, CANCELLED, REFUNDED
      0,  -- ReceiptStatus.REQUESTED
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
when (new.status in (3, 4, 7)) -- PaymentStatus.PAID, CANCELLED, REFUNDED
execute function tickets_v2_paymentstamp_create_receipt();

create table tickets_v2_receipt (
  id uuid not null,
  event_id integer not null,
  order_id uuid not null,
  correlation_id uuid not null,
  batch_id uuid,
  type tickets_v2_receipttype not null,
  status tickets_v2_receiptstatus not null default 0,
  email text not null default '',

  primary key (event_id, id),
  foreign key (event_id) references core_event (id),
  foreign key (event_id, order_id) references tickets_v2_order (event_id, id)
) partition by list (event_id);

create index tickets_v2_receipt_id_idx on tickets_v2_receipt (id);
create index tickets_v2_receipt_order_id_idx on tickets_v2_receipt (order_id);

create or replace function tickets_v2_receipt_notify_requested() returns trigger as $$
  begin
    perform pg_notify('tickets_v2_receipt', cast(new.event_id as text));
    return null;
  end;
$$ language plpgsql;

create or replace trigger notify_requested
after insert or update on tickets_v2_receipt
for each row
when (new.status = 0) -- ReceiptStatus.REQUESTED
execute function tickets_v2_receipt_notify_requested();
