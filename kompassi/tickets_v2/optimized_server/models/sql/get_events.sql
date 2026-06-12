select
  e.id,
  e.slug,
  e.name,
  m.provider_id,
  m.terms_and_conditions_url_en,
  m.terms_and_conditions_url_fi,
  m.terms_and_conditions_url_sv,
  coalesce(p.checkout_merchant, '') as paytrail_merchant,
  coalesce(p.checkout_password, '') as paytrail_password,
  o.name as organization_name,
  coalesce(m.contact_email, '') as contact_email,
  o.business_id as organization_business_id,
  m.cancellation_period_days,
  e.start_time
from
  core_event e
  join tickets_v2_ticketsv2eventmeta m on (e.id = m.event_id)
  join core_organization o on (e.organization_id = o.id)
  left join payments_paymentsorganizationmeta p on (o.id = p.organization_id)
