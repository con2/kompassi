# SQL files for hardened security configuration

Our strategy to database security in production deployments is as follows:

* Run database migrations with the `kompassi_ddl` user that owns the `kompassi` database and has wide privileges therein
* Perform day-to-day operation of the application with the `kompassi` user that only has `SELECT, CREATE, UPDATE, DELETE` privileges to most tables and even more restricted to some

## Restricted tables

* `django_migrations` – Why have anything else than `SELECT` here if you are not running migrations?
* `event_log_entry` – Contains the audit log. Read & append only. No deleting or changing rows.

## Scripts

### `01-setup-hardened-users.sql`

This script assumes that the database is called `kompassi` and it is initially owned by an user called `kompassi` that might or might not have superuser privileges.

Run this only once, as a superuser (eg. `postgres`), in the `kompassi` database, to revoke superuser privileges from `kompassi`, create a non-superuser `kompassi_ddl`, and switch the ownership of the `kompassi` database and all tables therein to them.

### `02-setup-privileges.sql`

This script assumes that the previous script has already been run, that is, there is a database called `kompassi` owned by the user `kompassi_ddl`, and there is an user called `kompassi` as well.

Run this script at the end of every migration, as the `kompassi_ddl` user, to grant the `kompassi` user the minimum sufficient permissions to be able to run the application.
