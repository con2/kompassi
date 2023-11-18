with status_counts_by_reference as (
  select
    reference,
    count(case when status = 'new' then 1 end) as num_new,
    count(case when status = 'ok' then 1 end) as num_ok,
    count(case when status = 'pending' then 1 end) as num_pending,
    count(case when status = 'fail' then 1 end) as num_fail,
    count(case when status = 'delayed' then 1 end) as num_delayed
  from
    payments_checkoutpayment
  where
    event_id = %s
  group by
    reference
)

select
  coalesce(sum(case when num_new > 0 and num_fail = 0 and num_ok = 0 then 1 else 0 end), 0) as new,
  coalesce(sum(case when num_fail > 0 and num_ok = 0 then 1 else 0 end), 0) as fail,
  coalesce(sum(case when num_fail > 0 and num_ok > 0 then 1 else 0 end), 0) as ok_after_fail,
  coalesce(sum(case when num_fail = 0 and num_ok > 0 then 1 else 0 end), 0) as ok_without_fail
from status_counts_by_reference;
