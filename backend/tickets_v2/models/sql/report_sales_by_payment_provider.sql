with orders_with_providers as (
  select
    o.id as order_id,
    o.cached_status as status,
    o.cached_price as price,
    any_value(ps.provider_id) as provider_id
  from
    tickets_v2_order o
    join tickets_v2_paymentstamp ps on (o.id = ps.order_id)
  where
    o.event_id = %(event_id)s
    and ps.event_id = %(event_id)s
  group by
    1, 2, 3
)
select
  pm.title as payment_provider,
  coalesce(sum(case when owp.status < 4 then owp.price else 0 end), 0) as total_sold,
  coalesce(sum(case when owp.status = 3 then owp.price else 0 end), 0) as total_paid
from
  jsonb_to_recordset(%(payment_providers)s::jsonb) as pm (id int, title text)
  join orders_with_providers owp on (pm.id = owp.provider_id)
group by
  1
