select
  1
from
  tickets_v2_order o
  left join tickets_v2_orderowner oo on (o.id = oo.order_id)
where
  oo.user_id is null and
  o.email = %s
limit 1
