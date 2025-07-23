with arrivals_by_hour as (
    select
        date_trunc('hour', arrived_at) as hour,
        count(*) as arrivals
    from
        badges_badge b
        join labour_personnelclass c on (b.personnel_class_id = c.id)
        join core_event e on (c.event_id = e.id)
    where
        e.slug = %s
        and b.revoked_at is null
    group by hour
    order by hour
)
select
    hour,
    arrivals,
    sum(arrivals) over (order by hour) as cum_arrivals
from
    arrivals_by_hour
