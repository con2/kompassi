-- NOTE: no PAID_AFTER_CANCELLATION bin here, unlike get_product_counters.sql. These
-- counters are derived from tickets_v2_ticket rows, and a flagged order holds none, so
-- it cannot appear in any of them by construction.
select
  q.id as quota_id,
  coalesce(
    sum(
      case
        when o.cached_status = 'PAID' then 1
        else 0
      end
    ),
    0
  ) as count_paid,
  coalesce(sum(case when t.order_id is not null then 1 else 0 end), 0) as count_reserved,
  coalesce(sum(case when t.order_id is null then 1 else 0 end), 0) as count_available
from
  tickets_v2_quota q
  left join tickets_v2_ticket t on (q.id = t.quota_id)
  left join tickets_v2_order o on (t.order_id = o.id and o.event_id = %(event_id)s)
where
  q.event_id = %(event_id)s and
  t.event_id = %(event_id)s
group by 1
