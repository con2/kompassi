select
  o.cached_price as total,
  o.order_number as order_number,
  o.language as language,
  p2.title,
  p2.price,
  p2.quantity,
  p2.vat_percentage,
  o.cached_status as status,
  exists (
    select 1
    from tickets_v2_paymentstamp ps
    where
      ps.event_id = o.event_id
      and ps.order_id = o.id
      and ps.status = 3 -- PaymentStatus.PAID
      and ps.provider_id <> 0 -- PaymentProvider.NONE
  ) as paid_by_provider
from
  tickets_v2_order o
  join lateral (
    select
      p.title,
      p.price,
      cast(pd.value as int) as quantity,
      p.vat_percentage
    from
      tickets_v2_product p
      join jsonb_each(o.product_data) pd on (cast(pd.key as int) = p.id)
  ) as p2 on true
where
  o.event_id = %(event_id)s
  and o.id = %(order_id)s
