with qualifying_receipts as (
  select
    r.id
  from
    tickets_v2_receipt r
  where
    r.event_id = %(event_id)s and
    r.status = 'REQUESTED' and
    r.batch_id is null
  limit (%(batch_size)s)
  for update
  skip locked
),

claimed_receipts as (
  update tickets_v2_receipt r
  set
    batch_id = %(batch_id)s,
    status = 'PROCESSING'
  from
    qualifying_receipts qr
  where
    r.event_id = %(event_id)s and
    r.id = qr.id
  returning
    r.id,
    r.order_id,
    r.type
)

select
  -- NOTE: fields returned must match the ReceiptPending class
  cr.id as receipt_id,
  cr.type as receipt_type,
  cr.order_id as order_id,
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
  claimed_receipts cr
  join tickets_v2_order o on (cr.order_id = o.id)
where
  o.event_id = %(event_id)s;
