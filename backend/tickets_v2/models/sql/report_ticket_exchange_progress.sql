select
  c.product_text,
  sum(case when c.status = 0 then 1 else 0 end) as not_exchanged,
  sum(case when c.status = 1 then 1 else 0 end) as exchanged,
  sum(case when c.status in (0, 1) then 1 else 0 end) as total
from
  lippukala_code c
  join lippukala_order o on (c.order_id = o.id)
where
  o.event = %(event_slug)s
group by
  c.product_text
