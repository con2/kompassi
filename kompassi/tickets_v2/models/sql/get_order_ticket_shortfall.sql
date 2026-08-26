-- Per-quota shortfall between what an order is expected to hold (from its
-- product_data) and what it currently holds. Mirrors the "expected"/"held"
-- CTEs of tickets_v2_ensure_tickets(); used by Order.fulfil() to know how
-- many tickets to mint into each quota before claiming them.
with expected as (
  select
    pq.quota_id,
    sum(cast(pd.value as int)) as quantity
  from
    tickets_v2_order o
    join jsonb_each(o.product_data) pd on true
    join tickets_v2_product_quotas pq on pq.product_id = cast(pd.key as int)
  where
    o.event_id = %(event_id)s
    and o.id = %(order_id)s
  group by
    pq.quota_id
),
held as (
  select
    quota_id,
    count(*) as quantity
  from
    tickets_v2_ticket
  where
    event_id = %(event_id)s
    and order_id = %(order_id)s
  group by
    quota_id
)
select
  expected.quota_id,
  expected.quantity - coalesce(held.quantity, 0) as quantity
from
  expected
  left join held on held.quota_id = expected.quota_id
where
  expected.quantity - coalesce(held.quantity, 0) > 0
