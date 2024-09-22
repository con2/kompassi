update tickets_v2_ticket t
set
  order_id = %(order_id)s
from
  jsonb_to_recordset(%(quantities_by_quota_id)s::jsonb) as q (quota_id int, quantity int)
  join lateral (
    select
      t.id as ticket_id
    from
      tickets_v2_ticket t
    where
      t.event_id = %(event_id)s
      and t.quota_id = q.quota_id
      and t.order_id is null
    limit q.quantity
    for update
    skip locked
  ) rt on true
where
  t.event_id = %(event_id)s
  and t.id = rt.ticket_id
returning t.id, t.event_id, t.quota_id, t.order_id;
