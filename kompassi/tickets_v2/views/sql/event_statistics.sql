with order_data as (
  select
    o.event_id,
    e.start_time::date as event_start_date,
    to_timestamp(
      ('x' || left(replace(o.id::text, '-', ''), 12))::bit(48)::bigint / 1000.0
    )::date as order_date,
    item.value::int * p.etickets_per_product as tickets_sold,
    p.price * item.value::int as amount
  from
    tickets_v2_order o
    join core_event e on (e.id = o.event_id)
    join lateral (
      select key, value from jsonb_each_text(o.product_data)
    ) item on true
    join tickets_v2_product p on (
      p.id = item.key::int
      and p.event_id = o.event_id
      and p.etickets_per_product > 0
    )
  where
    o.event_id = any(%s)
    and o.cached_status = 3  -- PAID
    and item.value::int > 0
)
select
  event_id,
  order_date,
  order_date - event_start_date as days_to_event,
  sum(tickets_sold) as total_tickets_sold,
  sum(amount) as total_amount
from order_data
group by event_id, event_start_date, order_date
order by event_id asc, days_to_event desc
