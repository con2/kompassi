with status_counts_by_order_id as (
  select
    order_id,
    count(case when status <= 1 then 1 end) as num_new, -- PaymentStatus.NOT_STARTED, PaymentStatus.PENDING
    count(case when status = 3 then 1 end) as num_ok,   -- PaymentStatus.OK
    count(case when status = 2 then 1 end) as num_fail  -- PaymentStatus.FAILED
  from
    tickets_v2_paymentstamp
  where
    event_id = %(event_id)s
    and type in (2, 3, 4, 5)  -- PaymentStampType.PAYMENT_REDIRECT, .PAYMENT_CALLBACK
    and provider_id = 1 -- PaymentProvider.PAYTRAIL
  group by
    order_id
)

select
  coalesce(sum(case when num_new > 0 and num_fail = 0 and num_ok = 0 then 1 else 0 end), 0) as new,
  coalesce(sum(case when num_fail > 0 and num_ok = 0 then 1 else 0 end), 0) as fail,
  coalesce(sum(case when num_fail > 0 and num_ok > 0 then 1 else 0 end), 0) as ok_after_fail,
  coalesce(sum(case when num_fail = 0 and num_ok > 0 then 1 else 0 end), 0) as ok_without_fail
from status_counts_by_order_id;
