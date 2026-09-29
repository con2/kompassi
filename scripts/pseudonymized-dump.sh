#!/bin/sh
# Writes a pseudonymized pg_dump (custom format) of a deployed Kompassi database to stdout:
#
#     scripts/pseudonymized-dump.sh > kompassi.pgdump
#     scripts/pseudonymized-dump.sh kompassi-staging > kompassi-staging.pgdump
#
# The personal data never leaves the cluster. A short-lived pod copies the database into a
# Postgres of its own, runs `manage.py pseudonymize_db` there, and only the result is streamed
# out. The pod is built from the pod template of the `kompassi` Deployment, so it runs the
# deployed image with the deployed configuration: the pseudonymization rules always match the
# schema they run against. Load the dump with scripts/load-dump.sh.
set -eu

namespace="${1:-kompassi-production}"
postgres_image=postgres:18
database=kompassi_pseudo
socket=/var/run/postgresql
pod="kompassi-pseudonymize-$(date +%Y%m%d%H%M%S)"

if [ -t 1 ]; then
  echo "$0: refusing to write a binary dump to a terminal; redirect stdout to a file" >&2
  exit 2
fi

log() {
  echo "==> $*" >&2
}

deployment="$(kubectl -n "$namespace" get deployment kompassi -o json)"

# The postgres container runs as the image's own postgres user because initdb needs the uid to
# have a passwd entry. It only listens on a socket shared with the pseudonymize container.
printf '%s' "$deployment" | jq \
  --arg pod "$pod" --arg postgres_image "$postgres_image" --arg database "$database" --arg socket "$socket" '
  .spec.template.spec as $spec
  | ($spec.containers[] | select(.name == "master")) as $backend
  | [$backend.env[] | select(.name | startswith("POSTGRES_"))] as $source
  | {
      apiVersion: "v1",
      kind: "Pod",
      metadata: {name: $pod, labels: {stack: "kompassi", component: "pseudonymize"}},
      spec: ($spec | del(.initContainers, .affinity, .terminationGracePeriodSeconds) + {
        restartPolicy: "Never",
        activeDeadlineSeconds: 7200,
        volumes: ($spec.volumes + [
          {name: "postgres-data", emptyDir: {}},
          {name: "postgres-socket", emptyDir: {}}
        ]),
        containers: [
          {
            name: "postgres",
            image: $postgres_image,
            command: ["sh", "-c", "initdb --auth=trust --username=postgres --encoding=UTF8 --locale-provider=icu --icu-locale=fi-FI -D /var/lib/postgresql/data && exec postgres -D /var/lib/postgresql/data -c listen_addresses= -c unix_socket_directories=\($socket)"],
            env: [$source[] | .name |= sub("^POSTGRES_"; "SOURCE_")],
            securityContext: ($backend.securityContext + {runAsUser: 999, runAsGroup: 999}),
            volumeMounts: [
              {name: "postgres-data", mountPath: "/var/lib/postgresql"},
              {name: "postgres-socket", mountPath: $socket},
              {name: "kompassi-temp", mountPath: "/tmp"}
            ]
          },
          ($backend | del(.args, .ports, .startupProbe, .readinessProbe, .livenessProbe, .lifecycle) + {
            name: "pseudonymize",
            command: ["sleep", "infinity"],
            env: ([.env[] | select(.name | startswith("POSTGRES_") | not)] + [
              {name: "POSTGRES_HOSTNAME", value: $socket},
              {name: "POSTGRES_DATABASE", value: $database},
              {name: "POSTGRES_USERNAME", value: "postgres"},
              {name: "POSTGRES_PASSWORD", value: ""},
              {name: "POSTGRES_SSLMODE", value: "disable"}
            ]),
            volumeMounts: (.volumeMounts + [{name: "postgres-socket", mountPath: $socket}])
          })
        ]
      })
    }
' | kubectl -n "$namespace" apply -f - >/dev/null

trap 'kubectl -n "$namespace" delete pod "$pod" --wait=false >/dev/null' EXIT

log "Waiting for pod $namespace/$pod"
kubectl -n "$namespace" wait --for=condition=Ready "pod/$pod" --timeout=300s >/dev/null
until kubectl -n "$namespace" exec "$pod" -c postgres -- pg_isready -q -h "$socket"; do
  sleep 2
done

log "Copying the $namespace database into the pod"
kubectl -n "$namespace" exec "$pod" -c postgres -- sh -c '
  set -eu
  createdb -h "$1" "$2"
  PGPASSWORD="$SOURCE_PASSWORD" pg_dump -Fc --no-owner --no-acl \
    "host=$SOURCE_HOSTNAME dbname=$SOURCE_DATABASE user=$SOURCE_USERNAME sslmode=$SOURCE_SSLMODE" \
    | pg_restore -h "$1" -d "$2" --no-owner --no-acl --exit-on-error
' sh "$socket" "$database" >&2

log "Pseudonymizing"
kubectl -n "$namespace" exec "$pod" -c pseudonymize -- python manage.py pseudonymize_db --yes >&2

log "Streaming the pseudonymized dump"
kubectl -n "$namespace" exec "$pod" -c postgres -- pg_dump -Fc --no-owner --no-acl -h "$socket" "$database"

log "Done"
