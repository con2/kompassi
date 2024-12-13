-- Not on the Critical Path but still happens during Hunger Games
-- Perhahs make it take event_id as input and filter on that
with qualifying_receipts as (
  select
    r.id
  from
    tickets_v2_receipt r
  where
    r.event_id = %(event_id)s and
    r.status = 0 and -- ReceiptStatus.REQUESTED
    r.batch_id is null
  limit %(batch_size)s
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
    r.correlation_id
)

select
  -- NOTE: fields returned must match the ReceiptPending class
  cr.id as receipt_id,
  cr.order_id as order_id,
  e.id as event_id,
  e.name as event_name,
  e.slug as event_slug,
  cr.correlation_id as correlation_id,
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
  join core_event e on (o.event_id = e.id)
where
  o.event_id = %(event_id)s;
