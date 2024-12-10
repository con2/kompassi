create index tickets_v2_order_email_idx on tickets_v2_order (email);

create table tickets_v2_orderowner (
  event_id integer not null,
  order_id uuid not null,
  user_id int not null,

  primary key (event_id, order_id),
  foreign key (event_id) references core_event (id),
  foreign key (event_id, order_id) references tickets_v2_order (event_id, id)
) partition by list (event_id);

create index on tickets_v2_orderowner (order_id);
create index on tickets_v2_orderowner (user_id);
