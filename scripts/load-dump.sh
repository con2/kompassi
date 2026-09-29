#!/bin/sh
# Replaces the docker compose development database with a dump from scripts/pseudonymized-dump.sh:
#
#     scripts/load-dump.sh kompassi.pgdump
#
# Pseudonymization leaves no usable passwords or OAuth2 client secrets, so afterwards this
# recreates the dev superuser mahti/mahti and the OAuth2 client of the local V2 frontend.
set -eu

if [ $# -ne 1 ]; then
  echo "usage: $0 DUMP_FILE" >&2
  exit 2
fi
dump="$1"

cd "$(dirname "$0")/.."

log() {
  echo "==> $*" >&2
}

log "Stopping the services that hold database connections"
docker compose up -d router postgres redis
docker compose stop backend worker uvicorn

log "Recreating the database"
until docker compose exec -T postgres pg_isready -q -U kompassi; do
  sleep 1
done
docker compose exec -T postgres dropdb -U kompassi --maintenance-db=postgres --if-exists --force kompassi
docker compose exec -T postgres createdb -U kompassi kompassi

log "Restoring $dump"
# Not with --jobs: a parallel restore creates the triggers of a partitioned table while its
# partitions are still loading, and the triggers fail on the rows being copied.
docker compose exec -T postgres pg_restore -U kompassi -d kompassi --no-owner --no-acl --exit-on-error <"$dump"

log "Migrating and recreating development credentials"
docker compose exec -T redis redis-cli -n 1 flushdb >/dev/null
docker compose run --rm --no-deps backend sh -c "python manage.py migrate && python manage.py setup_api_v2"

log "Done. Start the rest with: docker compose up"
