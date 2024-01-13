with arrivals_by_hour as (
    select
        date_trunc('hour', used_on) as hour,
        count(*) as arrivals
    from
        lippukala_code c
        join lippukala_order o on (c.order_id = o.id)
    where
        o.event = %s
        and c.status not in (2, 3)
    group by hour
    order by hour
)
select
    hour,
    arrivals,
    sum(arrivals) over (order by hour) as cum_arrivals
from
    arrivals_by_hour
