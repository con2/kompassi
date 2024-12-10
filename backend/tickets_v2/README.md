# Tickets V2

This is the V2 ticket shop, optimized for performance and reliability to withstand the Hunger Games.

## Definitions

**The Hunger Games**: The ticket sales of Tracon, during which thousands of tickets are sold within seconds.

**Critical Path**: The endpoints and operations that take place once or more per order during the Hunger Games. While the rest of Tickets V2 can be mostly YOLO'd with GraphQL, ORM etc, the Critical Path cannot afford such luxuries.

## Techniques employed

### Hand written SQL

We opt out of the Django ORM in situations where performance is paramount and instead write those queries in handcrafted optimized SQL.

### Partitioned tables

Most Tickets V2 tables are partitioned by event ID. This ensures the tables won't grow too big.

### `select … for update skip locked`

All salable tickets (to be accurate, instances of quotas; weekend ticket usually counts as one "ticket" of Fri, Sat, Sun each) are realized into the database as rows. An unassigned ticket has `order_id = null`. A product is shown if it is within its selling period and it has at least one unsold ticket remaining.

Tickets being reserved are explicitly locked using `select … for update skip locked` so as to allow operating concurrently within the `read committed` (Postgres default) transaction isolation level.

### Insert-only tables

Most tables (other than `tickets_v2_ticket`) are designed so that they would mostly be `insert` only ie. never be `update`d or `delete`d from. This is because the Postgres MVCC implementation causes updated rows to be slower to read until the next `vacuum`. This also applies to `delete`: while this is an oversimplification, suffice to say deleted rows are not actually deleted until the next `vacuum`, but a hidden field is updated to signify the row is deleted and should not be returned.

## Optimized server

Most of Kompassi code uses Django as its framework, and traditional blocking I/O. For the Critical path, we opt out of Django altogether and instead use FastAPI, `asyncio` and `psycopg` (3) in async mode to serve a simple REST/RPC API.

Code outside `tickets_v2.optimized_server` _may_ import code from within: for example, Pydantic models and enums may be generally useful.

The reverse is not true, however: `optimized_server` **MAY NOT** import anything that imports eg. `django.db.models` or otherwise requires `django.setup()` to have been run.

## Receipt worker

The receipt worker is run with `python manage.py tickets_v2_worker`. It listens to `notify tickets_v2_paymentstamp` events in Postgres and processes them in batches. Only one instance of the worker should be running at a time for now.

If multiple instances are desired, the approach should be changed to use `select … for update skip locked` so as to not allocate the same orders to multiple workers.
