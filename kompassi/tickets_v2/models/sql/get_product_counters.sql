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
        when op.status = 'PAID' then op.quantity
        else 0
      end
    ),
  0) as count_paid,
  coalesce(
    sum(
      case
        when op.status <= 'PAID' then op.quantity
        else 0
      end
    ),
  0) as count_reserved,
  -- Paid for, but holding no tickets: the payment landed after the order had already
  -- been cancelled and the quota had nothing left to give it back. Deliberately outside
  -- count_paid and count_reserved (the order holds nothing, so it must not affect
  -- availability arithmetic) but counted here so the money is not invisible.
  coalesce(
    sum(
      case
        when op.status = 'PAID_AFTER_CANCELLATION' then op.quantity
        else 0
      end
    ),
  0) as count_flagged,
  coalesce(sum(op.quantity), 0) as count_ever_reserved
from
  tickets_v2_product p
  left join order_products op on (op.product_id = p.id)
where
  p.event_id = %(event_id)s
group by 1;
