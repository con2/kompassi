with qualifying_receipts as (
  select
    r.id
  from
    tickets_v2_receipt r
  where
    r.event_id = %(event_id)s and
    r.status = 0 and -- ReceiptStatus.REQUESTED
    r.batch_id is null
  limit (%(batch_size)s)
  for update
  skip locked
),

claimed_receipts as (
  update tickets_v2_receipt r
  set
    batch_id = %(batch_id)s,
    status = 1 -- ReceiptStatus.PROCESSING
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
  o.cached_price as total_price
from
  claimed_receipts cr
  join tickets_v2_order o on (cr.order_id = o.id)
where
  o.event_id = %(event_id)s;
