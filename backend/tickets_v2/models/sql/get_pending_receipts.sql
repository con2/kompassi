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
  o.product_data,
  o.order_number,
  o.cached_price as total_price
from
  tickets_v2_order o
  join core_event e on (
    e.id = o.event_id
  )
  join tickets_v2_paymentstamp ps_paid on (
    ps_paid.event_id = o.event_id and
    ps_paid.order_id = o.id and
    ps_paid.status = 2 -- PaymentStatus.PAID
  )
  left join tickets_v2_paymentstamp ps_cancelled on (
    ps_cancelled.event_id = o.event_id and
    ps_cancelled.order_id = o.id and
    ps_cancelled.correlation_id = ps_paid.correlation_id and
    ps_cancelled.status = 3 -- PaymentStatus.CANCELLED
  )
  left join tickets_v2_receiptstamp rs_success on (
    rs_success.event_id = o.event_id and
    rs_success.order_id = o.id and
    rs_success.correlation_id = ps_paid.correlation_id and
    rs_success.type = 1 and -- ReceiptStampType.ORDER_CONFIRMATION
    rs_success.status = 2 -- ReceiptStatus.SUCCESS
  )
  -- NOTE: if multiple workers are added, also need to filter out ReceiptStampType.PROCESSING
where
  ps_cancelled.id is null and
  rs_success.id is null
limit %s;
