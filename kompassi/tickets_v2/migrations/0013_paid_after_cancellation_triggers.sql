-- Idempotently top an order up to its expected ticket complement, minting
-- nothing itself (that decision belongs to Order.fulfil()) — it only claims
-- from the free pool. Returns whether the order now holds everything it is
-- owed. Safe to call repeatedly (eg. once from the redirect stamp and once
-- from the callback stamp of the same payment): a second call finds no
-- shortfall and claims nothing.
--
-- All-or-nothing per call: a claim that cannot fully cover the shortfall is
-- rolled back (via the implicit subtransaction of the exception block below)
-- rather than left partially applied, so an order can never end up holding
-- some but not all of what it is owed — which would otherwise both defeat
-- idempotency (a second call would see different held/shortfall numbers) and
-- read as a conflict to tickets_v2_fsck, which expects a non-PAID order to
-- hold nothing.
--
-- A product may belong to many quotas; each unit sold consumes one ticket
-- from each of them. product_data keys may reference a superseded product
-- version — its tickets_v2_product_quotas rows still exist under the old
-- id, so the join resolves without following superseded_by.
create or replace function tickets_v2_ensure_tickets(p_event_id int, p_order_id uuid) returns boolean as $$
  declare
    v_shortfall bigint;
    v_claimed bigint;
    v_ok boolean;
  begin
    begin
      with expected as (
        select
          pq.quota_id,
          sum(cast(pd.value as int)) as quantity
        from
          tickets_v2_order o
          join jsonb_each(o.product_data) pd on true
          join tickets_v2_product_quotas pq on pq.product_id = cast(pd.key as int)
        where
          o.event_id = p_event_id
          and o.id = p_order_id
        group by
          pq.quota_id
      ),
      held as (
        select
          quota_id,
          count(*) as quantity
        from
          tickets_v2_ticket
        where
          event_id = p_event_id
          and order_id = p_order_id
        group by
          quota_id
      ),
      shortfall as (
        select
          expected.quota_id,
          expected.quantity - coalesce(held.quantity, 0) as quantity
        from
          expected
          left join held on held.quota_id = expected.quota_id
        where
          expected.quantity - coalesce(held.quantity, 0) > 0
      ),
      claimed as (
        update tickets_v2_ticket t
        set
          order_id = p_order_id
        from
          shortfall s
          join lateral (
            select
              t2.id as ticket_id
            from
              tickets_v2_ticket t2
            where
              t2.event_id = p_event_id
              and t2.quota_id = s.quota_id
              and t2.order_id is null
            limit s.quantity
            for update
            skip locked
          ) rt on true
        where
          t.event_id = p_event_id
          and t.id = rt.ticket_id
        returning
          t.id
      )
      select
        coalesce((select sum(quantity) from shortfall), 0),
        coalesce((select count(*) from claimed), 0)
      into
        v_shortfall,
        v_claimed;

      if v_claimed < v_shortfall then
        raise exception 'tickets_v2_ensure_tickets: insufficient tickets for order %', p_order_id;
      end if;

      v_ok := true;
    exception
      when others then
        v_ok := false;
    end;

    return v_ok;
  end;
$$ language plpgsql;

-- A PAID stamp landing on a CANCELLED (or already-flagged) order tops the
-- order back up from the free pool: fully covered -> PAID, otherwise flagged
-- PAID_AFTER_CANCELLATION for a human (or the frequent cron retry) to resolve.
-- Every other transition keeps the previous monotonic ratchet.
create or replace function tickets_v2_paymentstamp_update_order() returns trigger as $$
  begin
    update
      tickets_v2_order
    set
      cached_status = case
        when cached_status in ('CANCELLED', 'PAID_AFTER_CANCELLATION') and new.status = 'PAID' then
          case
            when tickets_v2_ensure_tickets(new.event_id, new.order_id) then 'PAID'::tickets_v2_paymentstatus
            else 'PAID_AFTER_CANCELLATION'::tickets_v2_paymentstatus
          end
        else new.status
      end
    where
      event_id = new.event_id and
      id = new.order_id and
      (
        (cached_status in ('CANCELLED', 'PAID_AFTER_CANCELLATION') and new.status = 'PAID')
        or cached_status < new.status
      );

    return null;
  end;
$$ language plpgsql;

-- Consult the order's cached_status (as trigger_00 just left it, trigger names
-- being executed in order) rather than the stamp's own status: a PAID stamp
-- that left the order PAID_AFTER_CANCELLATION must not create a receipt, since
-- that is what would otherwise email a valid e-ticket for an unfulfilled order.
create or replace function tickets_v2_paymentstamp_create_receipt() returns trigger as $$
  declare
    receipt_type tickets_v2_receipttype;
  begin
    if new.type = 'CREATE_REFUND_SUCCESS' then
      receipt_type := 'REFUNDED';
    elsif new.status = 'PAID' then
      if exists (
        select 1
        from tickets_v2_order o
        where
          o.event_id = new.event_id and
          o.id = new.order_id and
          o.cached_status = 'PAID'
      ) then
        receipt_type := 'PAID';
      else
        return null;
      end if;
    elsif new.status = 'REFUNDED' then
      receipt_type := 'REFUNDED';
    elsif new.status = 'CANCELLED' then
      -- Only notify cancellations of orders that were actually paid; abandoned
      -- unpaid orders are auto-cancelled by cron and must stay silent.
      if exists (
        select 1
        from tickets_v2_paymentstamp ps
        where
          ps.event_id = new.event_id and
          ps.order_id = new.order_id and
          ps.status = 'PAID'
      ) then
        receipt_type := 'CANCELLED';
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
      'REQUESTED',
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
