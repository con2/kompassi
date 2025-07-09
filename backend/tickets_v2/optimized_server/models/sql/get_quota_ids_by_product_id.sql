select
  product_id,
  array_agg(quota_id)
from
  tickets_v2_product_quotas pq
  join tickets_v2_product p on pq.product_id = p.id
where
  p.event_id = %s
group by product_id
