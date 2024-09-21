insert into tickets_v2_order (id, event_id, product_data, customer_data, cached_price)
select
  input.order_id,
  input.event_id,
  input.product_data,
  input.customer_data,
  price.total_price
from
  (values (%(order_id)s::uuid, %(event_id)s::int, %(product_data)s::jsonb, %(customer_data)s::jsonb))
    input (order_id, event_id, product_data, customer_data)
  join lateral (
    select
      sum(cast(pd.value as numeric) * product.price) as total_price
    from
      tickets_v2_product product
      join jsonb_each(input.product_data) pd on (cast(pd.key as int) = product.id)
    where
      product.event_id = %(event_id)s
  ) as price on true
returning event_id, id;
