# Restoring deleted program offers from a PITR restore

This runbook covers recovering program offers (and everything that cascaded from their deletion)
after they were deleted via the `DeleteProgramOffers` GraphQL mutation
(`kompassi/program_v2/graphql/mutations/delete_program_offers.py`) — whether by mistake or
maliciously. It uses the `program_v2_restore_deleted_program_offers` management command together
with a Point-In-Time-Recovery (PITR) restore of the database taken from before the deletion.

The event log (`event_log_v2`) will contain an entry like this when this has happened:

```
entry type = program_v2.program_offer.deleted
other fields = {"event": "<event_slug>", "context": "...", "organization": "...", "count_deleted": <n>}
```

Note that the log entry does **not** record which rows were deleted, only the count. The restore
process below determines the exact set of affected rows by diffing IDs between the PITR restore
and the current database, rather than trusting the log.

## What actually gets deleted

Program offers are `forms.Response` rows (survey responses to a survey with
`app_name=program_v2`, `purpose_slug=default`). Deleting them is a real SQL `DELETE`, which
cascades through foreign keys:

| Table | Relation | `on_delete` | Effect |
|---|---|---|---|
| `forms_response` | — | — | the program offers themselves, plus any superseded old revisions |
| `forms_responsedimensionvalue` | `subject → Response` | `CASCADE` | deleted with the response |
| `involvement_involvement` | `response → Response` | `CASCADE` | deleted, but only `PROGRAM_OFFER`-type involvements — the mutation detaches (nulls `response_id` on) `PROGRAM_HOST` involvements first, so those are *not* deleted |
| `involvement_involvementdimensionvalue` | `subject → Involvement` | `CASCADE` | deleted transitively with the involvements above |
| `program_v2_program` | `program_offer → Response` | **`SET_NULL`** | **not deleted** — but any offer that had already been accepted into a `Program` now has `program_offer_id = NULL`. This is easy to miss and must be relinked, not just re-inserted. |

`forms.Response` and `forms.ResponseDimensionValue`/`involvement.InvolvementDimensionValue` use
UUID or database-assigned primary keys that are never reused after a delete, so restoring rows
with their original IDs cannot collide with anything created after the incident. This is what
makes an in-place restore (rather than a full database rollback) safe.

## 1. Take a PITR restore of the database into a side instance

Restore to a target time a few seconds *before* the deletion. Given a log timestamp of
`2026-07-25 09:28:43.704 UTC`, target e.g. `2026-07-25 09:28:41 UTC`.

Afterwards, confirm on the side instance that the `program_v2.program_offer.deleted` entry is
**absent** from `event_log_v2` — that proves the restore stopped short of the delete transaction.
Do not restore into or over the production database — this must be a separate, standalone
instance.

## 2. Take a fresh backup of production

Before running anything against production, take a fresh backup/snapshot distinct from the PITR
side instance, so that the restore procedure itself can be undone if something turns out to be
wrong with it.

## 3. Point the backend at the side instance via the `pitr` database alias

`kompassi/settings.py` wires up an optional second database alias named `pitr` when
`PITR_POSTGRES_HOSTNAME` is set (following the same `PITR_POSTGRES_HOSTNAME` /
`PITR_POSTGRES_DATABASE` / `PITR_POSTGRES_USERNAME` / `PITR_POSTGRES_PASSWORD` /
`PITR_POSTGRES_PORT` / `PITR_POSTGRES_SSLMODE` naming as the main `POSTGRES_*` settings). Set
these to point at the side instance from wherever you'll run `manage.py` against production, e.g.:

```bash
export PITR_POSTGRES_HOSTNAME=<side-instance-host>
export PITR_POSTGRES_DATABASE=<side-instance-db-name>
export PITR_POSTGRES_USERNAME=<read-only-user>
export PITR_POSTGRES_PASSWORD=<...>
```

A read-only user on the side instance is sufficient and preferred — the command never writes to
the `pitr` alias, only to `default`.

## 4. Dry run

```bash
python manage.py program_v2_restore_deleted_program_offers <event_slug> --expected-count <count_deleted from the log entry>
```

Without `--commit`, the command performs the entire restore inside a transaction and then rolls it
back, so you can review what it *would* do first. It reports:

- how many responses exist on `pitr` but are missing on `default` (what will be restored)
- how many responses exist on `default` but not on `pitr` (created/edited after the PITR snapshot —
  left untouched)
- counts for each table it restores or relinks

Pass `--expected-count` set to `count_deleted` from the event log entry as a cross-check: the
command refuses to proceed if the number of rows it would restore doesn't match exactly. If it
doesn't match, stop and investigate before proceeding — don't just drop `--expected-count` to make
it pass.

## 5. Commit

Once the dry run's counts look right:

```bash
python manage.py program_v2_restore_deleted_program_offers <event_slug> --expected-count <count_deleted> --commit
```

This is safe to run against a live production database — it only inserts rows that don't already
exist and relinks `program_offer_id` where it is currently `NULL`; it never deletes or overwrites
existing rows. It re-derives `cached_dimensions`/`cached_key_fields` on the restored responses and
involvements from the (now restored) dimension values rather than trusting whatever was cached in
the PITR snapshot.

The command is idempotent — running it again afterwards (with or without `--commit`) reports
nothing left to restore.

## 6. Verify and clean up

- Spot-check a few restored offers via the admin UI or GraphQL.
- Re-check `event_log_v2` if you want to record that the incident was remediated.
- Once you're confident, tear down the PITR side instance and unset the `PITR_POSTGRES_*`
  variables — don't leave `pitr` wired up to a stale side instance.

## Rehearsing this before touching production

Before running any of this against production, rehearse it against a disposable copy: clone the
current database into a second one on the same Postgres server (e.g. `pg_dump | psql` into a new
database), point `pitr` at *that*, delete a handful of program offers for a test event the same
way `DeleteProgramOffers` does, and confirm the command restores them correctly and idempotently.
This is exactly how the command was validated during development.
