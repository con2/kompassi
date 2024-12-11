with orders_with_status as (
  select
    o.id,
    max(ps.status) as status
  from
    tickets_v2_order o
    left join tickets_v2_paymentstamp ps on (ps.order_id = o.id)
  where
    o.event_id = %(event_id)s and
    ps.event_id = %(event_id)s
  group by 1
)

select
  q.id as quota_id,
  coalesce(sum(case when t.order_id is not null and os.status = 2 then 1 else 0 end), 0) as count_paid,
  coalesce(sum(case when t.order_id is not null then 1 else 0 end), 0) as count_reserved,
  coalesce(sum(case when t.order_id is null then 1 else 0 end), 0) as count_available
from
  tickets_v2_quota q
  left join tickets_v2_ticket t on (q.id = t.quota_id)
  left join orders_with_status os on (os.id = t.order_id)
where
  q.event_id = %(event_id)s and
  t.event_id = %(event_id)s
group by 1
