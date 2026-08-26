with status_counts_by_order_id as (
  select
    order_id,
    count(case when status <= 'PENDING' then 1 end) as num_new,
    count(case when status = 'PAID' then 1 end) as num_ok,
    count(case when status = 'FAILED' then 1 end) as num_fail
  from
    tickets_v2_paymentstamp
  where
    event_id = %(event_id)s
    and type in (
      'CREATE_PAYMENT_SUCCESS', 'CREATE_PAYMENT_FAILURE', 'PAYMENT_REDIRECT', 'PAYMENT_CALLBACK'
    )
    and provider = 'PAYTRAIL'
  group by
    order_id
)

select
  coalesce(sum(case when num_new > 0 and num_fail = 0 and num_ok = 0 then 1 else 0 end), 0) as new,
  coalesce(sum(case when num_fail > 0 and num_ok = 0 then 1 else 0 end), 0) as fail,
  coalesce(sum(case when num_fail > 0 and num_ok > 0 then 1 else 0 end), 0) as ok_after_fail,
  coalesce(sum(case when num_fail = 0 and num_ok > 0 then 1 else 0 end), 0) as ok_without_fail
from status_counts_by_order_id;
