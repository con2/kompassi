with numbered_programme_roles as (
    select
        *,
        row_number() over (partition by (programme_id, person_id) order by (id)) as row_number
    from
        programme_programmerole pr
)
select
    id
from
    numbered_programme_roles
where
    row_number > 1
