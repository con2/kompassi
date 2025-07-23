drop trigger trigger_90_create_receipt
on tickets_v2_paymentstamp;

create trigger trigger_90_create_receipt
after insert on tickets_v2_paymentstamp
for each row
when (new.status in (3, 7)) -- PaymentStatus.PAID, REFUNDED
execute function tickets_v2_paymentstamp_create_receipt();
