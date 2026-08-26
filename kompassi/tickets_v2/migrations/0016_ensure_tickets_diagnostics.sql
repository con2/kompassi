-- Same as the 0013 version of tickets_v2_ensure_tickets, except that the
-- "not enough tickets in the free pool" case is now raised with a
-- distinguishable errcode and is the *only* condition silently reported as
-- false. Anything else — a lock timeout, a serialization failure, a
-- product_data value that is not an integer — used to be swallowed by
-- `when others`, indistinguishably from a genuine shortfall, permanently
-- flagging the order PAID_AFTER_CANCELLATION with no trace of why. Those now
-- leave a warning in the log before we give up on them.
--
-- We still never let the exception escape: this runs inside the payment
-- callback's transaction, and aborting that would lose the payment stamp.
--
-- Idempotently tops an order up to its expected ticket complement, minting
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
        -- Expected outcome, not a fault: the quota has nothing left to give.
        -- 'TKTS1' is in the user-defined SQLSTATE space (class TK is unassigned).
        raise exception 'tickets_v2_ensure_tickets: insufficient tickets for order % (short %, claimed %)',
          p_order_id, v_shortfall, v_claimed
          using errcode = 'TKTS1';
      end if;

      v_ok := true;
    exception
      when sqlstate 'TKTS1' then
        v_ok := false;
      when others then
        raise warning 'tickets_v2_ensure_tickets failed unexpectedly for order % in event %: % (%)',
          p_order_id, p_event_id, sqlerrm, sqlstate;
        v_ok := false;
    end;

    return v_ok;
  end;
$$ language plpgsql;
