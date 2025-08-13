with payment_attempts_by_payment_method_and_status as (
  select
    correlation_id,
    any_value(data ->> 'checkout-provider')::text as payment_method,
    max(status) as status
  from
    tickets_v2_paymentstamp
  where
    event_id = %(event_id)s
    and provider_id = 1 -- PaymentProvider.PAYTRAIL
    and type in (4, 5) -- PaymentStampType.PAYMENT_REDIRECT, .PAYMENT_CALLBACK
  group by
    correlation_id
),
payment_attempt_counts as (
  select
    payment_method,
    sum(case when status = 3 then 1 else 0 end) as ok,     -- PaymentStatus.PAID
    sum(case when status = 2 then 1 else 0 end) as failed, -- PaymentStatus.FAILED
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
