# Kubernetes deployment for kompassi

Generate Kubernetes manifests using

    ENV=dev node --experimental-strip-types manifest.mts

This runs `kubernetes/manifest.mts`, a brutally simple Node.js program with no
dependencies other than `fs`. It accepts one environment variable, `ENV`, with
the values `dev` (the default), `staging` and `production`, and outputs
Kubernetes manifests as JSON files in the directory it was run in (so `cd
kubernetes` first, or run it from there as above).

Test with Skaffold (with Docker Desktop or similar local Kubernetes cluster):

    skaffold dev

For staging and production, deployment is done in two steps using Skaffold:

    cd kubernetes && ENV=staging node --experimental-strip-types manifest.mts && cd -
    skaffold build --file-output build.json
    skaffold deploy -n kompassi-staging -a build.json

See `skaffold.yaml` in the repository root. `skaffold build` remains valid for
manual/local use; CI builds the image with `docker buildx` instead (see
`.github/workflows/backend.yaml`) and hand-writes `build.json` in the format
`skaffold deploy -a` expects, since it no longer invokes `skaffold build`.

You should, for the most part, not deploy manually. GitHub Actions CI/CD is
set up to deploy all commits to `main` into staging (https://dev.kompassi.eu)
and, after a manual gate, into production (https://kompassi.eu). See
`.github/workflows/backend.yaml`.

See `kompassi-v2-frontend/kubernetes/manifest.ts` for a smaller sibling
example of the same approach (see https://github.com/japsu/depleten for the
underlying philosophy) — this one has more moving parts because the Django
backend has more workloads (gunicorn, celery, the newer background worker,
uvicorn for tickets_v2, the nightly cron job) and supports both a
self-managed (local dev) and externally-managed (staging, production)
Postgres/Redis/Secret. Static files are served by WhiteNoise from within the
Django process, so there is no separate static-file workload.
