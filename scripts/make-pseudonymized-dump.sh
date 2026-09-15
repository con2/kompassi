#!/usr/bin/env bash
# Usage: scripts/make-pseudonymized-dump.sh
#
# Creates a pseudonymized dump of the production database.
# Run on the production server (SSH in or docker exec into the app container).
#
# Authentication uses PostgreSQL standard environment variables and ~/.pgpass —
# set PGHOST, PGPORT, PGUSER, PGPASSWORD as needed, or configure ~/.pgpass.
# PGDATABASE must be set to the production database name.
#
# The pseudonymized dump is written to /tmp and its path is printed at the end.
set -euo pipefail

ORIG_DB="${PGDATABASE:?PGDATABASE must be set to the production database name}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
PSEUDO_DB="${ORIG_DB}_pseudo_${TIMESTAMP}"
OUTPUT_FILE="/tmp/${PSEUDO_DB}.sql.gz"

echo "==> Creating temp database ${PSEUDO_DB}"
createdb "${PSEUDO_DB}"

echo "==> Copying ${ORIG_DB} -> ${PSEUDO_DB} (pg_dump -Fc | pg_restore)"
# Binary custom format: compressed, faster than plain SQL, safe for same-server copies.
# For large databases with a maintenance window available, replace this with:
#   createdb -T "${ORIG_DB}" "${PSEUDO_DB}"
# For maximum throughput without downtime, use directory format with --jobs=N instead of piping.
pg_dump --format=custom "${ORIG_DB}" \
  | pg_restore --dbname="${PSEUDO_DB}" --no-owner --no-privileges

echo "==> Pseudonymizing ${PSEUDO_DB}"
# Override POSTGRES_DATABASE so Django connects to the temp copy, not the original.
# PGDATABASE is intentionally left unchanged so pg_* tools still default to the original DB.
POSTGRES_DATABASE="${PSEUDO_DB}" python manage.py pseudonymize_db --yes

echo "==> Dumping pseudonymized database"
pg_dump "${PSEUDO_DB}" | gzip >"${OUTPUT_FILE}"

echo "==> Cleaning up ${PSEUDO_DB}"
dropdb "${PSEUDO_DB}"

echo "Done. Pseudonymized dump: ${OUTPUT_FILE}"
