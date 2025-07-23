# Database stuff

## Development environment quick-start SQL schema dump

The file `00-schema.sql` contains a A schema snapshot from some point in time. This is used to speed up setting up the development environment from scratch as running all 300+ migrations takes multiple minutes.

There may or may not be migrations newer than this; `python manage.py docker_start` will run `setup` (including `migrate`) if there are no `Event`s in the database, indicating first start-up.

To refresh the schema snapshot, run `migrate` (NOTE: not `setup`) on an empty database and then dump it like this:

    # WARNING! This nukes your current development database
    docker compose down -v
    docker compose run --rm backend python manage.py migrate
    docker compose exec postgres pg_dump -Ox -U kompassi > kompassi/sql/00-schema.sql

    # Then test it before committing
    docker compose down -v
    docker compose up --build

## Hardened security configuration

**NOTE: Since moving to QB & Siilo, this hardened security configuration is currently not in use and the `kompassi` user is used for both DDL & normal operation.**

Our strategy to database security in production deployments is as follows:

- Run database migrations with the `kompassi_ddl` user that owns the `kompassi` database and has wide privileges therein
- Perform day-to-day operation of the application with the `kompassi` user that only has `SELECT, CREATE, UPDATE, DELETE` privileges to most tables and even more restricted to some

This is not used in the development environment.

### Restricted tables

- `django_migrations` – Why have anything else than `SELECT` here if you are not running migrations?
- `django_admin_log` – Contains actions performed in the Django Admin UI. No deleting or changing rows.
- `event_log_entry` – Contains the audit log. Read & append only. No deleting or changing rows.

### Scripts

#### `01-setup-hardened-users.sql`

This script assumes that the database is called `kompassi` and it is initially owned by an user called `kompassi` that might or might not have superuser privileges.

Run this only once, as a superuser (eg. `postgres`), in the `kompassi` database, to revoke superuser privileges from `kompassi`, create a non-superuser `kompassi_ddl`, and switch the ownership of the `kompassi` database and all tables therein to them.

#### `02-setup-privileges.sql`

This script assumes that the previous script has already been run, that is, there is a database called `kompassi` owned by the user `kompassi_ddl`, and there is an user called `kompassi` as well.

Run this script at the end of every migration, as the `kompassi_ddl` user, to grant the `kompassi` user the minimum sufficient permissions to be able to run the application.
