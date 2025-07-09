select o.*
from
  core_event e
  join tickets_v2_order o on (e.id = o.event_id)
  join tickets_v2_orderowner oo on (
    o.event_id = oo.event_id and
    o.id = oo.order_id
  )
where
  e.slug = %(event_slug)s and
  oo.user_id = %(user_id)s and
  o.id = %(order_id)s
