with order_lines as (
  select o.id as order_id, p.vat_percentage as vat_rate,
         sum(p.price * pd.quantity::numeric) as gross
  from tickets_v2_order o
  join lateral jsonb_each_text(o.product_data) as pd(product_id, quantity) on true
  join tickets_v2_product p on p.id = pd.product_id::int
  where o.event_id = %(event_id)s and pd.quantity::int > 0 and p.vat_percentage > 0
  group by 1, 2
),
paid as (
  select
    order_id,
    to_char(
      date_trunc(
        'month',
        to_timestamp(
          ('x' || left(replace(min(id::text), '-', ''), 12))::bit(48)::bigint / 1000.0
        ) at time zone %(event_timezone)s
      ),
      'YYYY-MM'
    ) as month
  from tickets_v2_paymentstamp
  where event_id = %(event_id)s and status = 'PAID'
  group by order_id
),
refunded as (
  select
    order_id,
    to_char(
      date_trunc(
        'month',
        to_timestamp(
          ('x' || left(replace(min(id::text), '-', ''), 12))::bit(48)::bigint / 1000.0
        ) at time zone %(event_timezone)s
      ),
      'YYYY-MM'
    ) as month
  from tickets_v2_paymentstamp
  where event_id = %(event_id)s and status = 'REFUNDED'
  group by order_id
),
movements as (
  select paid.month, ol.vat_rate, ol.gross as amount, 1 as sign
  from order_lines ol join paid using (order_id)
  union all
  select refunded.month, ol.vat_rate, ol.gross, -1
  from order_lines ol join paid using (order_id) join refunded using (order_id)
)
select
  month, vat_rate,
  sum(case when sign > 0 then amount else 0 end) as sold,
  sum(case when sign < 0 then -amount else 0 end) as returned,
  sum(sign * amount) as net,
  sum(sign * round(amount * vat_rate / (100 + vat_rate), 2)) as vat
from movements
group by 1, 2
order by 1, 2
