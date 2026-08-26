# tickets_v2 load testing

Procedure for measuring the tickets_v2 hot path (`POST /api/tickets-v2/{event_slug}/orders/`)
under a thundering-herd on-sale, and for A/B-comparing two branches against the same
synthetic event. This document exists because the harness that makes this possible
(`tickets_v2_emloaden`) rotted silently for 18 months — see "History" below — and the
fix is only durable if the procedure for using it is written down somewhere other than
one person's shell history.

## Target

Derived from the real tracon2026 on-sale (below): sustain **≥60 orders/sec** with
**p95 ≤ 3s** on the buy leg, all the way through quota exhaustion, with no measurable
regression against `main` at the same offered load.

## Components

All under `kompassi/tickets_v2/management/commands/`:

- `tickets_v2_setup_performance_test` — a normal Django management command. Seeds a
  synthetic `perftest` event (its own `Organization`/`Venue`/`Event`, never a real one)
  with quotas and products mirroring the real tracon2026 shape. Idempotent: re-running it
  resizes quotas via `Quota.set_quota()` without disturbing already-claimed tickets, and
  it never truncates or otherwise touches any other event's data — safe to run against a
  database that also has the production dump loaded.
- `tickets_v2_emloaden` — **not** a management command, invoke with
  `python -m kompassi.tickets_v2.management.commands.tickets_v2_emloaden`. The load
  generator: an open-loop arrival model (buyers are launched on a schedule regardless of
  whether the server has finished with earlier buyers) driving a basket model derived
  from the real on-sale.
- `tickets_v2_fsck` — a normal Django management command,
  `python manage.py tickets_v2_fsck perftest`. Confirms every order's ticket count
  matches what its `product_data` implies. Run after every load test.

## Quick start (against the local docker-compose stack)

```bash
docker compose up -d
docker compose exec backend python manage.py migrate
docker compose exec backend python manage.py tickets_v2_setup_performance_test --really
docker compose exec backend python -m kompassi.tickets_v2.management.commands.tickets_v2_emloaden \
  --rate 5 --duration-seconds 10
docker compose exec backend python manage.py tickets_v2_fsck perftest
```

A short smoke run like the one above should report `SUCCESS` for substantially all
buyers and zero `UNEXPECTED_ERROR` — that outcome is what proves the API-key fix is in
place and that a `401` (or any other unforeseen response) can no longer hide silently,
which is exactly the failure mode that broke this harness for 18 months undetected.

`tickets_v2_emloaden` flags:

| Flag | Default | Meaning |
|---|---|---|
| `--base-url` | `$BASE_URL` or `http://localhost:7998` | optimized_server root |
| `--event-slug` | `perftest` | |
| `--processes` | `4` | worker processes; each gets `--rate / --processes` orders/sec |
| `--rate` | `60.0` | target orders/sec offered at plateau |
| `--ramp-seconds` | `5.0` | linear ramp from 0 to `--rate` |
| `--duration-seconds` | `150.0` | total offered-load duration (ramp included) |
| `--seed` | `0` | seeds the buyer-plan RNG; same seed ⇒ same buyer sequence |
| `--json-out` | none | write a machine-readable report, for A/B diffing |
| `--api-key` | `$KOMPASSI_TICKETS_V2_API_KEY` or `secret` | |

To reach a real sell-out at the default quota sizes (5300/5300/5300/1000), a run needs
several minutes at `--rate 60`; scale quotas down while iterating on the harness itself:

```bash
docker compose exec backend python manage.py tickets_v2_setup_performance_test --really --quota-scale 0.1
docker compose exec backend python -m kompassi.tickets_v2.management.commands.tickets_v2_emloaden \
  --rate 30 --duration-seconds 60 --processes 4 --seed 42 --json-out /tmp/report.json
```

## Where the numbers come from

The production dump `kompassi-20260730.sql`, mounted into the local `postgres` service,
contains the real tracon2026 on-sale (2026-07-12 15:00 UTC). Order ids are UUIDv7, whose
first 48 bits are a millisecond timestamp, so creation time is recoverable without any
extra column:

```sql
-- reusable expression: UUIDv7 -> creation timestamp
to_timestamp((('x' || substr(replace(id::text, '-', ''), 1, 12))::bit(48)::bigint) / 1000.0)
```

**Orders are counted regardless of current `cached_status`.** An order row only exists
once `reserve_tickets.sql` has actually claimed tickets, so existence — not status — is
what "successful" means here; a since-cancelled or since-refunded order still
represents real hot-path contention at the moment it was placed.

Orders per minute, opening 6 minutes (verified against the dump on 2026-08-26 — the
table below and everything derived from it should be treated as reproducible, not
frozen: re-run these queries against a newer dump before the next on-sale and update
this document):

```sql
select
  date_trunc('minute', to_timestamp((('x' || substr(replace(id::text, '-', ''), 1, 12))::bit(48)::bigint) / 1000.0)) as minute,
  count(*) as orders
from tickets_v2_order_tracon2026
where to_timestamp((('x' || substr(replace(id::text, '-', ''), 1, 12))::bit(48)::bigint) / 1000.0)
      >= '2026-07-12 15:00:00+00'
  and to_timestamp((('x' || substr(replace(id::text, '-', ''), 1, 12))::bit(48)::bigint) / 1000.0)
      < '2026-07-12 15:06:00+00'
group by 1
order by 1;
```

| Measure | Real value |
|---|---|
| Orders in minute 1 | **1992** (then 512, 102, 41, 45, 51) |
| Peak successful orders/sec | **61/s at t+15s**; 40–55/s sustained through t+30s |
| Ticket rows claimed in minute 1 | ~13 500 (~225 row UPDATEs/sec) |
| Share of inventory sold in minute 1 | ~80% of 16 900 tickets |
| Quotas | Fri/Sat/Sun 5300 each; Iltabileet 1000 (**sold out**) |
| `max_per_order` | 5, on every product |

These are **successful orders only**: a buyer who got `409 NOT_ENOUGH_TICKETS`, or who
only browsed, leaves no row, so this is a floor on the true offered request rate, not
the rate itself.

Basket composition in the opening minute (products keyed by title, joined through
`product_data`):

```sql
with orders as (
  select o.id, o.product_data
  from tickets_v2_order_tracon2026 o
  where to_timestamp((('x' || substr(replace(o.id::text, '-', ''), 1, 12))::bit(48)::bigint) / 1000.0)
        >= '2026-07-12 15:00:00+00'
    and to_timestamp((('x' || substr(replace(o.id::text, '-', ''), 1, 12))::bit(48)::bigint) / 1000.0)
        < '2026-07-12 15:01:00+00'
)
select
  p.title,
  count(distinct o.id) as orders_containing,
  sum((pd.value)::int) as units,
  round(avg((pd.value)::int), 2) as avg_qty
from orders o
cross join lateral jsonb_each_text(o.product_data) as pd(product_id, value)
join tickets_v2_product p on p.id = pd.product_id::int
group by p.title
order by orders_containing desc;
```

| Product | Orders containing | Units | Avg qty |
|---|---|---|---|
| Viikonloppulippu (**spans all three day quotas**) | 1717 | 4146 | 2.41 |
| K18 Iltabilelippu | 266 | 592 | 2.23 |
| Lauantailippu | 178 | 329 | 1.85 |
| Sunnuntailippu | 46 | 87 | 1.89 |
| Perjantailippu | 32 | 46 | 1.44 |

88% of orders contain exactly one product, 12% two, 3 orders had three (query: count
`jsonb_object_keys(product_data)` per order, group by count). Weekend ticket quantity
histogram (same query restricted to `p.title = 'Viikonloppulippu'`, grouped by
quantity): `{1: 496, 2: 586, 3: 267, 4: 163, 5: 205}`.

All of the figures above are reproduced exactly by the queries as written (verified
2026-08-26) and are the ones baked into `tickets_v2_emloaden`'s `CATEGORY_WEIGHTS` /
`QUANTITY_HISTOGRAM` constants. If you refresh them from a newer dump, update both this
document and those constants together.

## The basket and arrival models

`tickets_v2_emloaden` decides every buyer's arrival time and basket **upfront**, in a
single-threaded pass driven by `random.Random(seed + worker_index)`, before spawning any
coroutines. This is what makes `--seed` actually reproducible: if the RNG were instead
consumed by buyer coroutines as they ran, the interleaving of concurrent requests would
make draw order (and so the resulting sequence) nondeterministic even for a fixed seed.

- **Arrival model**: Poisson thinning. Candidate arrivals are drawn from a homogeneous
  Poisson process at the peak rate; each is kept with probability `rate_at(t) / rate`,
  where `rate_at` ramps linearly over `--ramp-seconds` and then holds constant. This is
  open-loop — arrivals do not wait for earlier buyers to finish — which is what lets the
  generator offer more load than the server can absorb. A closed-loop generator (wait
  for buyer N before launching N+1) cannot do this, and so under-reports latency
  collapse by construction.
- **Basket model**: each buyer picks one category (weekend/iltabileet/saturday/sunday/
  friday) from the weights above (renormalised to sum to 1), a quantity from the weekend
  histogram (reused for every category — it is the only per-unit distribution the source
  query produced), and with probability 0.12 a second category + quantity. A small
  `JUST_BROWSING_PROBABILITY` (0.05, not measurable from successful-orders-only data —
  browsers leave no row — so treat as a conservative placeholder) sends some buyers away
  without attempting a purchase. Categories are matched against live product titles at
  request time (case-insensitive substring), so the same buyer plan works unchanged
  against both the real tracon2026 catalogue and the `perftest` catalogue.

## The local A/B procedure

The two branches under comparison may have **different database schemas** — on this
branch, `main` and `feat/tickets-fulfil` differ by migration `0011_native_enums.sql` —
so this is not a code swap. For each branch:

1. `docker compose down -v && docker compose up -d --build` (postgres runs on tmpfs, so
   every run starts from a cold, identical page cache and reloads the mounted dump).
2. `docker compose exec backend python manage.py migrate`
3. `docker compose exec backend python manage.py tickets_v2_setup_performance_test --really`
4. `docker compose exec postgres psql -U kompassi -c "create extension if not exists pg_stat_statements;"`
   then `select pg_stat_statements_reset();`
5. `docker compose exec postgres psql -U kompassi -c 'vacuum analyze tickets_v2_ticket, tickets_v2_order;'`
   so both branches start from fresh planner statistics.
6. Offer the load with a fixed `--seed`.
7. `docker compose exec backend python manage.py tickets_v2_fsck perftest` — must report
   no conflicts.
8. Archive the `--json-out` output plus a `pg_stat_statements` snapshot (query below).

**Five repetitions per branch**, alternating branches rather than doing all of one then
all of the other, so laptop thermal drift does not correlate with branch. Report medians
and the spread; a difference smaller than the run-to-run spread is not a finding. Leave
autovacuum at defaults (it's part of what's being measured), but record
`autovacuum_count` so a run where it fired mid-sale can be identified.

The harness itself is the thing most likely to be wrong, so verify every run: `fsck`
clean; outcome counts sum to buyers launched; `sold + free = total` per quota (query
below).

### Server-side instrumentation

```sql
-- top 20 hot-path statements
select
  round(total_exec_time::numeric, 2) as total_ms,
  calls,
  round(mean_exec_time::numeric, 3) as mean_ms,
  round(stddev_exec_time::numeric, 3) as stddev_ms,
  rows, shared_blks_hit, shared_blks_read,
  left(query, 60) as query
from pg_stat_statements
order by total_exec_time desc
limit 20;

-- HOT-update ratio: selling a ticket moves an index entry from the free-pool partial
-- index (tickets_v2_ticket_quota_id_idx, where order_id is null) to the claimed-ticket
-- partial index (tickets_v2_ticket_order_id_idx, where order_id is not null), which by
-- definition cannot be a HOT update -- this ratio is the direct measure of that churn.
select relname, n_tup_upd, n_tup_hot_upd,
  round(100.0 * n_tup_hot_upd / nullif(n_tup_upd, 0), 1) as hot_pct,
  n_dead_tup, autovacuum_count
from pg_stat_user_tables
where relname like 'tickets_v2_%'
order by n_tup_upd desc;

-- sold + free = total per quota (same query the app uses,
-- kompassi/tickets_v2/models/sql/get_quota_counters.sql, event_id filled in for perftest)
select
  q.id as quota_id,
  q.name,
  coalesce(sum(case when t.order_id is not null then 1 else 0 end), 0) as sold,
  coalesce(sum(case when t.order_id is null then 1 else 0 end), 0) as free
from tickets_v2_quota q
left join tickets_v2_ticket t on t.quota_id = q.id
where q.event_id = (select id from core_event where slug = 'perftest')
group by 1, 2
order by 2;
```

Also capture `docker stats` for the `postgres` and `uvicorn` containers so client-side
and server-side saturation can be told apart. **Prove which side is the bottleneck**
before trusting any number: if the generator's own CPU is pegged, or achieved rate
tracks offered rate exactly up to a ceiling that does not move when uvicorn workers are
doubled, the client is the limiter and the run is meaningless. On a laptop running
postgres, uvicorn and the generator all at once, this is the likeliest first finding —
budget for running the generator from a second machine, or capping `--processes`.

Two connection-pool knobs exist purely so a run can *distinguish* "the SQL is slow" from
"we ran out of connections" — neither is an optimisation, and both default to unset,
which reproduces today's behaviour (`min_size=4`, `max_size` unset → effectively 4) so
leaving them alone changes nothing. To test a different pool size, add
`TICKETS_V2_POOL_MIN_SIZE` / `TICKETS_V2_POOL_MAX_SIZE` to the `uvicorn` service's
`environment:` block in `docker-compose.yml` and `docker compose restart uvicorn`;
record the value used in every run. At 60 orders/sec × ~5 statements/order, the default
`4 connections/worker × 8 workers = 32` against Postgres's `max_connections=100` may
itself be the limiter, independent of any SQL — this is exactly what these knobs exist
to confirm or rule out.

## Scenarios beyond the happy path

- **`cron_frequent` under load**: run
  `while true; do docker compose exec backend python manage.py cron_frequent; sleep 30; done`
  in a sidecar shell for the duration of a sale run, and diff the result against the same
  run without it. This is the most likely real regression on this branch, because
  `Order.cancel_unpaid_orders()` does a per-event `.count()` plus a per-order
  `cancel_and_refund()` transaction, and `Order.retry_paid_after_cancellation()` scans
  every event's partition with no `event_id` predicate. Running it every 30s instead of
  the production 5min compresses a long sale's worth of interference into one run.
- **paid-after-cancellation under load**: `tickets_v2_ensure_tickets` cannot be reached
  through the null payment provider used by the load test, since there is no real
  callback to replay. Drive it directly instead: after a sell-out run, cancel a batch of
  orders, then call `Order.fulfil()` / `Order.retry_paid_after_cancellation()` over N
  orders concurrently and time them, with `pg_stat_statements` isolating the function
  body. This measures the function and its per-call savepoint without pretending it is
  on the order-creation hot path — it is reached only from
  `cached_status IN ('CANCELLED', 'PAID_AFTER_CANCELLATION') AND new.status = 'PAID'` in
  `trigger_00_update_order`, from `Order.fulfil()`, and from
  `Order.retry_paid_after_cancellation()`.

## Staging soak

Once the local A/B is clean, run one dress rehearsal on `dev.kompassi.eu` before the next
real on-sale. Differences from local:

- Use the **synthetic `perftest` event only** — never a real event slug.
- Suspend the `cron-frequent` CronJob for events other than `perftest`, or accept and
  record its interference; `concurrencyPolicy: "Forbid"` means it cannot pile up.
- Real network latency and Kubernetes resource limits are the point; record pod CPU
  throttling alongside the same `pg_stat_statements` snapshot.
- Run the generator from outside the cluster so client and server are genuinely separate
  machines — this is also the run that settles whether the laptop was the limiter
  locally.
- Record the same `--json-out` so local and staging runs are directly comparable.

## Recorded baseline

**Not yet performed: the formal 5-repetition local A/B between `main` and
`feat/tickets-fulfil`** described above. That requires checking out and rebuilding each
branch in turn and running five alternating sell-out repetitions per branch, which is a
substantial dedicated session on its own — run it with the exact steps in "The local A/B
procedure" before relying on this document for a go/no-go call, and record the result
here.

What *has* been run, as part of reviving the harness (2026-08-26, `feat/tickets-fulfil`,
laptop, `--quota-scale 0.1`, `--rate 30 --ramp-seconds 5 --duration-seconds 60
--processes 4 --seed 42`, single run, not a median of five — treat as a smoke test that
the harness produces sane numbers, not as a baseline):

```
Buyers launched: 1713
Results:
  SUCCESS: 276
  JUST_BROWSING: 748
  NOT_ENOUGH_TICKETS: 6
  SERVED_SOLD_OUT_PAGE: 683

time_loading_products:  p50 0.0050s  p95 0.0112s  p99 0.0162s
time_buying_tickets:    p50 0.0038s  p95 0.0129s  p99 0.0206s
time_viewing_order_page: p50 0.0016s  p95 0.0055s  p99 0.0074s
```

`tickets_v2_fsck perftest` reported zero conflicts; `sold` exactly matched `total` on
every quota (530/530/530/100). `pg_stat_statements` after the run showed the
`list_products` query (which checks `EXISTS (... order_id is null)` per quota) as the
single largest time sink at this quota scale (1713 calls, 1.07s total), ahead of
`reserve_tickets.sql` itself (282 calls, 0.25s total) — expected, since most buyers here
hit the products page and then found nothing available (`SERVED_SOLD_OUT_PAGE`) rather
than reaching the buy leg. The HOT-update ratio on `tickets_v2_ticket_perftest` was
**0.0%** (0 of 1708 updates), confirming the partial-index churn hypothesis: every ticket
sale moves an index entry from the free-pool partial index to the order-id partial index,
which by definition cannot be a HOT update.

This run does not by itself say anything about `feat/tickets-fulfil` vs `main` — it only
confirms the harness now runs end-to-end, reproduces sell-out correctly (no oversell),
and that the instrumentation queries above return real data. The comparison this
document exists to support is still open.

## Accepted coverage gaps

- **Zero-price only.** `NullProvider` refuses non-zero prices, so the benchmark measures
  a 4-statement transaction where production runs 5 (`get_order.sql` is skipped) and
  then makes an external Paytrail HTTP call outside the transaction. The missing
  statement's cost can be read separately from `pg_stat_statements` on any real-price
  traffic; the Paytrail call is network-bound and outside the lock window, so it does not
  affect contention.
- **No payment callbacks.** The redirect/callback routes and their trigger work are not
  exercised by the sale scenario, only by the targeted scenario above.
- **Successful orders only in the real baseline.** The 1992-orders/minute figure omits
  409s and browsers, so it is a floor on the real offered rate, not the rate itself.

## History

`tickets_v2_emloaden` / `tickets_v2_setup_performance_test` / `tickets_v2_fsck` had no
semantic change between 2024-12-10 and this revision — the only 2025–2026 touches were
the `backend/` → `kompassi/` package move and a `ruff` autofix. The harness stopped
working on 2024-12-26 (commit `449276de1`), the day all three optimized_server endpoints
gained mandatory `x-api-key` verification: the load generator sent no API key, so its
first request 401'd, and because `asyncio.gather` was called without
`return_exceptions=True`, that single 401 crashed the entire run instead of being counted
as an outcome. Nobody ran it again for 18 months. The lesson generalised into the harness
itself: `UNEXPECTED_ERROR` now exists specifically so the next unforeseen failure mode is
a number in the results table, not a silent, permanent stop.
