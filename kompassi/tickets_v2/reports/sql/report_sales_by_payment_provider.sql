with orders_with_providers as (
  select
    o.id as order_id,
    o.cached_status as status,
    o.cached_price as price,
    any_value(ps.provider) as provider
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
  coalesce(sum(case when owp.status < 'CANCELLED' then owp.price else 0 end), 0) as total_sold,
  coalesce(sum(case when owp.status = 'PAID' then owp.price else 0 end), 0) as total_paid,
  -- Money received for orders whose payment landed after cancellation and that hold no
  -- tickets. Outside total_sold and total_paid (nothing was delivered) but not invisible.
  coalesce(sum(case when owp.status = 'PAID_AFTER_CANCELLATION' then owp.price else 0 end), 0) as total_flagged
from
  jsonb_to_recordset(%(payment_providers)s::jsonb) as pm (id text, title text)
  join orders_with_providers owp on (pm.id::tickets_v2_paymentprovider = owp.provider)
group by
  1
