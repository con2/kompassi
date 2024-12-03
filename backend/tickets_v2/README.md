# Tickets V2

## Note about `optimized_server`

Most of Kompassi code uses Django as its framework, and traditional blocking I/O.

Tickets V2 has a server component that is optimized for SPEED. Hence it uses FastAPI, `asyncio` and `psycopg` (3) in async mode.

Code outside `tickets_v2.optimized_server` _may_ import code from within: for example, Pydantic models and enums may be generally useful.

The reverse is not true, however: `optimized_server` **MAY NOT** import anything that imports eg. `django.db.models` or otherwise requires `django.setup()` to have been run.
