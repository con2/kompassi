from pathlib import Path

from django.db import migrations

# Restores the 0013 body verbatim: `when others` swallowing every failure as a plain
# "not enough tickets", with no diagnostic.
REVERSE_SQL = """
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
"""


class Migration(migrations.Migration):
    dependencies = [  # noqa: RUF012
        ("tickets_v2", "0015_alter_paymentstamp_data"),
    ]

    operations = [  # noqa: RUF012
        migrations.RunSQL(
            sql=Path(__file__).with_name("0016_ensure_tickets_diagnostics.sql").read_text(),
            reverse_sql=REVERSE_SQL,
        ),
    ]
