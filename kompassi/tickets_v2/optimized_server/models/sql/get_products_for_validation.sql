select
  id,
  superseded_by_id,
  available_from,
  available_until
from
  tickets_v2_product
where
  event_id = %(event_id)s
  and id = any(%(product_ids)s)
