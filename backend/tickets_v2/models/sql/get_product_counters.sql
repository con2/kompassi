with qualifying_orders as (
  select
    o.id,
    o.product_data,
    max(ps.status) as status -- PaymentStatus: REFUNDED > CANCELLED > PAID > PENDING
  from
    tickets_v2_order o
    join tickets_v2_paymentstamp ps on (ps.order_id = o.id)
  where
    o.event_id = %(event_id)s and
    ps.event_id = %(event_id)s
  group by 1, 2
  having
    max(ps.status) <= 2 -- PaymentStatus.PENDING or PAID
),

order_products as (
  select
    qo.status,
    cast(op_json.key as int) as product_id,
    cast(op_json.value as int) as quantity
  from
    qualifying_orders qo
    join jsonb_each(qo.product_data) op_json on true
)

select
  -- group all versions of product under current
  coalesce(p.superseded_by_id, p.id) as product_id,
  coalesce(sum(case when op.status = 2 then op.quantity else 0 end), 0) as amount_paid,
  coalesce(sum(op.quantity), 0) as amount_reserved
from
  tickets_v2_product p
  left join order_products op on (op.product_id = p.id)
where
  p.event_id = %(event_id)s
group by 1;
