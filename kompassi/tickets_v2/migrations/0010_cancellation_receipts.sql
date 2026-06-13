-- Make a customer/admin cancellation always leave a final receipt (which the
-- receipt worker emails and the admin UI shows), without re-spamming the orders
-- that the cron auto-cancels.
--
-- Background: 0001 created a receipt for any PAID/CANCELLED/REFUNDED stamp. 0007
-- dropped CANCELLED so that auto-cancelled *unpaid* orders would not email their
-- customers. That left two gaps for deliberate cancellations of *paid* orders:
--
--   1. Free (zero-price) orders are cancelled without refund -> CANCELLED stamp,
--      which 0007 made silent.
--   2. Provider refunds only record CREATE_REFUND_SUCCESS (status REFUND_REQUESTED)
--      synchronously; the REFUNDED stamp -- the only one that created a receipt --
--      arrives later via Paytrail's async refund callback (and never in dev).
--
-- Fix: create the receipt as soon as the outcome is known:
--   - PAID                       -> PAID receipt (order confirmation, unchanged)
--   - REFUNDED                   -> REFUNDED receipt (manual refund / refund callback)
--   - CREATE_REFUND_SUCCESS      -> REFUNDED receipt (provider accepted the refund)
--   - CANCELLED, if order was paid -> CANCELLED receipt
--
-- The receipt id is the stamp correlation_id. A provider refund's request, success
-- and callback stamps all share one correlation_id, so the eventual REFUNDED
-- callback dedupes against the receipt created at CREATE_REFUND_SUCCESS time (one
-- email, not two). Failed refunds (CREATE_REFUND_FAILURE / REFUND_FAILED) never
-- match, so a failed refund is never announced as done.

create or replace function tickets_v2_paymentstamp_create_receipt() returns trigger as $$
  declare
    receipt_type smallint;
  begin
    if new.type = 8 then -- PaymentStampType.CREATE_REFUND_SUCCESS
      receipt_type := 7; -- ReceiptType.REFUNDED
    elsif new.status = 3 then -- PaymentStatus.PAID
      receipt_type := 3; -- ReceiptType.PAID
    elsif new.status = 7 then -- PaymentStatus.REFUNDED
      receipt_type := 7; -- ReceiptType.REFUNDED
    elsif new.status = 4 then -- PaymentStatus.CANCELLED
      -- Only notify cancellations of orders that were actually paid; abandoned
      -- unpaid orders are auto-cancelled by cron and must stay silent.
      if exists (
        select 1
        from tickets_v2_paymentstamp ps
        where
          ps.event_id = new.event_id and
          ps.order_id = new.order_id and
          ps.status = 3 -- PaymentStatus.PAID
      ) then
        receipt_type := 4; -- ReceiptType.CANCELLED
      else
        return null;
      end if;
    else
      return null;
    end if;

    insert into tickets_v2_receipt (
      event_id,
      id,
      order_id,
      correlation_id,
      type,
      status,
      email
    )
    select
      new.event_id,
      new.correlation_id, -- one receipt per correlation_id (dedupes refund success vs callback)
      new.order_id,
      new.correlation_id,
      receipt_type,
      0, -- ReceiptStatus.REQUESTED
      o.email
    from
      tickets_v2_order o
    where
      o.event_id = new.event_id and
      o.id = new.order_id
    on conflict (event_id, id) do nothing;

    return null;
  end;
$$ language plpgsql;

drop trigger trigger_90_create_receipt
on tickets_v2_paymentstamp;

create trigger trigger_90_create_receipt
after insert on tickets_v2_paymentstamp
for each row
-- PaymentStatus.PAID, CANCELLED, REFUNDED or PaymentStampType.CREATE_REFUND_SUCCESS
when (new.status in (3, 4, 7) or new.type = 8)
execute function tickets_v2_paymentstamp_create_receipt();
