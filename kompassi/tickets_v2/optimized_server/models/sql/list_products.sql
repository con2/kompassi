with quota_availability as (
  select
    quota.id as quota_id,
    exists (
      select 1
      from
        tickets_v2_ticket t
      where
        t.event_id = %(event_id)s
        and t.quota_id = quota.id
        and t.order_id is null
      limit 1
    ) as available
  from
    tickets_v2_quota quota
  where
    quota.event_id = %(event_id)s
)
select
  p.id,
  p.title,
  p.description,
  p.price,
  p.max_per_order,
  bool_and(qa.available) as available
from
  tickets_v2_product p
  join tickets_v2_product_quotas pq on pq.product_id = p.id
  join quota_availability qa on qa.quota_id = pq.quota_id
where
  p.event_id = %(event_id)s
  and p.superseded_by_id is null
  and p.available_from <= now()
  and (p.available_until is null or p.available_until > now())
group by 1, 2, 3, 4, 5
order by p.ordering;
