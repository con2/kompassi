create table tickets_v2_order (
  id uuid not null,
  event_id integer not null,
  user_id integer null,
  paid_at timestamp with time zone null,
  cancelled_at timestamp with time zone null,
  cached_price numeric(10, 2) not null,
  product_data jsonb not null,
  first_name text not null,
  last_name text not null,
  phone text not null,
  email text not null,

  primary key (event_id, id),
  foreign key (event_id) references core_event (id) deferrable initially deferred
) partition by list (event_id);

create index on tickets_v2_order (id);

create table tickets_v2_ticket (
  id uuid not null,
  event_id integer not null,
  quota_id integer not null,
  order_id uuid,

  primary key (event_id, id),
  foreign key (event_id) references core_event (id),
  foreign key (event_id, order_id) references tickets_v2_order (event_id, id)
) partition by list (event_id);

create index on tickets_v2_ticket (id);
create index on tickets_v2_ticket (order_id) where order_id is not null;
create index on tickets_v2_ticket (quota_id) where order_id is null;
