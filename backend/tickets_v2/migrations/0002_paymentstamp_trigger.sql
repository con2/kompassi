create or replace function tickets_v2_paymentstamp_notify_paid() returns trigger as $$
begin
  notify tickets_v2_paymentstamp;
  return null;
end;
$$ language plpgsql;

create or replace trigger notify_paid
after insert on tickets_v2_paymentstamp
for each row
when (new.status = 2) -- PaymentStatus.PAID
execute function tickets_v2_paymentstamp_notify_paid();
