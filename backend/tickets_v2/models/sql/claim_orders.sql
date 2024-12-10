insert into tickets_v2_orderowner (event_id, order_id, user_id)
select
  e.id,
  o.id,
  %(user_id)s
from
  core_event e
  join tickets_v2_order o on e.id = o.event_id
  left join tickets_v2_orderowner oo on (
    e.id = oo.event_id and
    o.id = oo.order_id
  )
where
  oo.user_id is null and
  o.email = %(email)s
