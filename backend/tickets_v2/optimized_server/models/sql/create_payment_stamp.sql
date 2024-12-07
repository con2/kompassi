insert into tickets_v2_paymentstamp (
  id,
  event_id,
  order_id,
  provider,
  type,
  status,
  correlation_id,
  data
) values (
  %s,
  %s,
  %s,
  %s,
  %s,
  %s,
  %s,
  %s
)
