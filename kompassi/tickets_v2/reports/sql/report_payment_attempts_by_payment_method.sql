with payment_attempts_by_payment_method_and_status as (
  select
    correlation_id,
    any_value(data ->> 'checkout-provider')::text as payment_method,
    max(status) as status
  from
    tickets_v2_paymentstamp
  where
    event_id = %(event_id)s
    and provider = 'PAYTRAIL'
    and type in ('PAYMENT_REDIRECT', 'PAYMENT_CALLBACK')
  group by
    correlation_id
),
payment_attempt_counts as (
  select
    payment_method,
    sum(case when status = 'PAID' then 1 else 0 end) as ok,
    sum(case when status = 'FAILED' then 1 else 0 end) as failed,
    count(*) as total
  from
    payment_attempts_by_payment_method_and_status
  group by
    payment_method
  order by total desc
)
select
  payment_method,
  ok,
  failed,
  failed::float/total as failed_ratio,
  total
from
  payment_attempt_counts
