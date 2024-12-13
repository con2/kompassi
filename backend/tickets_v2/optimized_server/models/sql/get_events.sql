select
  e.id,
  e.slug,
  e.name,
  m.provider_id,
  coalesce(p.checkout_merchant, '') as paytrail_merchant,
  coalesce(p.checkout_password, '') as paytrail_password
from
  core_event e
  join tickets_v2_ticketsv2eventmeta m on (e.id = m.event_id)
  join core_organization o on (e.organization_id = o.id)
  left join payments_paymentsorganizationmeta p on (o.id = p.organization_id)
