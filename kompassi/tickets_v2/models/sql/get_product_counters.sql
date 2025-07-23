with order_products as (
  select
    o.cached_status as status,
    cast(op_json.key as int) as product_id,
    cast(op_json.value as int) as quantity
  from
    tickets_v2_order o
    join jsonb_each(o.product_data) op_json on true
  where
    o.event_id = %(event_id)s
)

select
  -- group all versions of product under current
  coalesce(p.superseded_by_id, p.id) as product_id,
  coalesce(
    sum(
      case
        when op.status = 3 then op.quantity -- PaymentStatus.PAID
        else 0
      end
    ),
  0) as count_paid,
  coalesce(
    sum(
      case
        when op.status <= 3 then op.quantity -- PaymentStatus.PAID
        else 0
      end
    ),
  0) as count_reserved,
  coalesce(sum(op.quantity), 0) as count_ever_reserved
from
  tickets_v2_product p
  left join order_products op on (op.product_id = p.id)
where
  p.event_id = %(event_id)s
group by 1;
