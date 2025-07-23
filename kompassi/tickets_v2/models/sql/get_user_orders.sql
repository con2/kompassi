select o.*
from
  tickets_v2_order o
  join tickets_v2_orderowner oo on (
    o.event_id = oo.event_id and
    o.id = oo.order_id
  )
where
  oo.user_id = %(user_id)s
