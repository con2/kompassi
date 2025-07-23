select
  e.id as event_id,
  o.payment_date as sales_date,
  (o.payment_date - e.start_time::date) as days_to_event,
  sum(op.count * p.electronic_tickets_per_product) as total_tickets_sold,
  sum(p.price_cents * op.count) as total_amount_cents
from
  tickets_order o
  join tickets_orderproduct op on o.id = op.order_id
  join tickets_product p on op.product_id = p.id
  join core_event e on o.event_id = e.id
where
  e.id = any (%s)
  -- and e.start_time is not null -- already filtered in e.id = …
  and o.confirm_time is not null
  and o.payment_date is not null
  and o.cancellation_time is null
  and p.electronic_ticket = true
group by 1, 2, 3
order by 1 asc, 3 desc;
