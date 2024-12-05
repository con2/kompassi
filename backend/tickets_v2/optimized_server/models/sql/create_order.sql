insert into tickets_v2_order (
  id,
  event_id,
  cached_price,
  product_data,
  language,
  first_name,
  last_name,
  email,
  phone
)
select
  input.order_id,
  input.event_id,
  price.total_price,
  input.product_data,
  input.language,
  input.first_name,
  input.last_name,
  input.email,
  input.phone
from
  (values (
    %s::uuid,
    %s::int,
    %s::jsonb,
    %s,
    %s,
    %s,
    %s,
    %s
  )) input (
    order_id,
    event_id,
    product_data,
    language,
    first_name,
    last_name,
    email,
    phone
  )
  join lateral (
    select
      sum(cast(pd.value as numeric) * product.price) as total_price
    from
      tickets_v2_product product
      join jsonb_each(input.product_data) pd on (cast(pd.key as int) = product.id)
    where
      product.event_id = input.event_id
  ) as price on true
returning event_id, id, cached_price, order_number;
