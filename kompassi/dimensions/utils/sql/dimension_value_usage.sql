with response_dimension_value_usage as (
  select
    dv.id as value_id,
    count(*) as count_subjects
  from
    forms_responsedimensionvalue rdv
    join dimensions_dimensionvalue dv on dv.id = rdv.value_id
    join dimensions_dimension d on d.id = dv.dimension_id
  where
    d.universe_id = %(universe_id)s
  group by 1
),
involvement_dimension_value_usage as (
  select
    dv.id as value_id,
    count(*) as count_subjects
  from
    involvement_involvementdimensionvalue idv
    join dimensions_dimensionvalue dv on dv.id = idv.value_id
    join dimensions_dimension d on d.id = dv.dimension_id
  where
    d.universe_id = %(universe_id)s
  group by 1
),
program_dimension_value_usage as (
  select
    dv.id as value_id,
    count(*) as count_subjects
  from
    program_v2_programdimensionvalue pdv
    join dimensions_dimensionvalue dv on dv.id = pdv.value_id
    join dimensions_dimension d on d.id = dv.dimension_id
  where
    d.universe_id = %(universe_id)s
  group by 1
),
schedule_item_dimension_value as (
  select
    dv.id as value_id,
    count(*) as count_subjects
  from
    program_v2_scheduleitemdimensionvalue sdv
    join dimensions_dimensionvalue dv on dv.id = sdv.value_id
    join dimensions_dimension d on d.id = dv.dimension_id
  where
    d.universe_id = %(universe_id)s
  group by 1
)
select
  d.id,
  dv.id as value_id,
  coalesce(rdvs.count_subjects, 0) as response_count,
  coalesce(idvs.count_subjects, 0) as involvement_count,
  coalesce(pdvs.count_subjects, 0) as program_count,
  coalesce(sdvs.count_subjects, 0) as schedule_item_count
from
  dimensions_dimension d
  join dimensions_dimensionvalue dv on dv.dimension_id = d.id
  left join response_dimension_value_usage rdvs on rdvs.value_id = dv.id
  left join involvement_dimension_value_usage idvs on idvs.value_id = dv.id
  left join program_dimension_value_usage pdvs on pdvs.value_id = dv.id
  left join schedule_item_dimension_value sdvs on sdvs.value_id = dv.id
where
  d.universe_id = %(universe_id)s
