# Apps we can't remove due to cross-application references

Would need to forcibly squash migrations to get rid of these as they are depended upon by migrations in other applications.

## enrollment

Stripped down to a stub (only `models/`, `migrations/`, `apps.py`) because 24 event apps'
`SignupExtra.special_diet` M2M fields, and 31 of their migration files, target
`enrollment.SpecialDiet`. Retiring the app label entirely would need every one of those
migrations rewritten to point at a new home for `SpecialDiet`, which makes already-applied
event migrations depend on an unapplied one and trips Django's `InconsistentMigrationHistory`
check on every existing database. The only ways around that are a one-time `migrate --fake` on
every existing database, or keeping the label alive — hence the stub.

To remove it for good: move `SpecialDiet` (and the abstract `SimpleChoice` it and `ConconPart`
descended from) into `labour`, keeping `db_table = "enrollment_specialdiet"`; add a `labour`
migration that creates that table via `SeparateDatabaseAndState` (state-only `CreateModel` +
`RunSQL("CREATE TABLE IF NOT EXISTS ...")` so fresh databases get it without touching existing
ones); repoint the 31 event migrations' app-label dependency and `to=` references from
`enrollment` to `labour`, and the ~15 `from kompassi.zombies.enrollment.models import
SimpleChoice, SpecialDiet` imports; then delete this app. Every existing database then needs
`python manage.py migrate labour <new_migration> --fake` run before the normal `migrate`, or
`migrate` fails with `InconsistentMigrationHistory`. Orphaned `enrollment` rows in
`django_migrations`/`django_content_type` are harmless afterward.
