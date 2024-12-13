-- FIXME scans all event partitions of the order table
-- Not on the Critical Path but still happens during Hunger Games
-- Perhahs make it take event_id as input and filter on that
select distinct on (o.id, ps_paid.correlation_id)
  -- NOTE: fields returned must match the ReceiptPending class
  o.id as order_id,
  e.id as event_id,
  e.name as event_name,
  e.slug as event_slug,
  ps_paid.correlation_id,
  o.language,
  o.first_name,
  o.last_name,
  o.email,
  o.phone,
  o.product_data,
  o.order_number,
  o.cached_price as total_price
from
  tickets_v2_order o
  join core_event e on (
    e.id = o.event_id
  )
  left join tickets_v2_receipt rs_success on (
    rs_success.event_id = o.event_id and
    rs_success.order_id = o.id and
    rs_success.correlation_id = ps_paid.correlation_id and
    rs_success.type = 1 and -- ReceiptStampType.ORDER_CONFIRMATION
    rs_success.status = 2 -- ReceiptStatus.SUCCESS
  )
  -- NOTE: if multiple workers are added, also need to filter out ReceiptStampType.PROCESSING
where
  o.cached_status < 3 and -- PaymentStatus.PAID
  rs_success.id is null
limit %s;
