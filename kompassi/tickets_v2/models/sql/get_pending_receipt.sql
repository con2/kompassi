select
  -- NOTE: fields returned must match the PendingReceipt class
  r.id as receipt_id,
  r.type as receipt_type,
  r.order_id as order_id,
  o.event_id as event_id,
  o.language,
  o.first_name,
  o.last_name,
  o.email,
  o.phone,
  o.product_data,
  o.order_number,
  o.cached_price as total_price,
  exists (
    select 1
    from tickets_v2_paymentstamp ps
    where
      ps.event_id = o.event_id
      and ps.order_id = o.id
      and ps.status = 'PAID'
      and ps.provider <> 'NONE'
  ) as paid_by_provider,
  exists (
    select 1
    from lippukala_code c
    join lippukala_order lo on (c.order_id = lo.id)
    where
      lo.reference_number = cast(o.id as text)
      and c.status = 1 -- lippukala.consts.USED
  ) as has_used_etickets
from
  tickets_v2_receipt r
  join tickets_v2_order o on (o.event_id = r.event_id and o.id = r.order_id)
where
  r.event_id = %(event_id)s
  and r.id = %(receipt_id)s;
