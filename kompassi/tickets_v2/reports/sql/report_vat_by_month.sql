select
  to_char(
    date_trunc(
      'month',
      to_timestamp(
        ('x' || left(replace(o.id::text, '-', ''), 12))::bit(48)::bigint / 1000.0
      ) at time zone %(event_timezone)s
    ),
    'YYYY-MM'
  ) as year_month,
  p.vat_percentage,
  sum(p.price * pd.quantity::numeric * p.vat_percentage / (100 + p.vat_percentage)) as vat_amount
from
  tickets_v2_order o
  join lateral jsonb_each_text(o.product_data) as pd(product_id, quantity) on true
  join tickets_v2_product p on p.id = pd.product_id::int
where
  o.event_id = %(event_id)s
  and o.cached_status = any(%(paid_statuses)s)
  and pd.quantity::int > 0
  and p.vat_percentage > 0
group by 1, 2
order by 1, 2
