select
  o.cached_price as total,
  o.order_number as order_number,
  o.language as language,
  p2.title,
  p2.price,
  p2.quantity,
  (
    select max(ps.status)
    from tickets_v2_paymentstamp ps
    where
      ps.event_id = %(event_id)s
      and ps.order_id = %(order_id)s
  ) as status,
  o.last_name,
  o.first_name,
  o.email,
  o.phone
from
  tickets_v2_order o
  join lateral (
    select
      p.title,
      p.price,
      cast(pd.value as int) as quantity
    from
      tickets_v2_product p
      join jsonb_each(o.product_data) pd on (cast(pd.key as int) = p.id)
  ) as p2 on true
where
  o.event_id = %(event_id)s
  and o.id = %(order_id)s
