# Migrate Kompassi production media from Minio to Garage

Runbook for moving the `kompassi` bucket from `minio.con2.fi` (MinIO, discontinued upstream) to
`garage.con2.fi` (Garage on the qb cluster, see `infrastructure/kubernetes/garage.README.md`).
Staging (`dev.kompassi.eu`, bucket `kompassidev`) went through the same steps on 2026-09-28; the
manifest and the URL rewrite command from that move are already on `main`.

## What uses the bucket

Two code paths, both configured by the same `MINIO_*` environment variables in
`kubernetes/manifest.mts` and both building their own boto3 client:

- **Django media storage** (`STORAGES["default"]`, django-storages `S3Boto3Storage`): event
  logos, carousel slides, external event logos, paikkala icons, emprinten data. Stores object keys
  only and presigns URLs at render time, so it needs no data fix after the move.
- **Form file uploads** (`kompassi/forms/utils/s3_presign.py`): the browser gets a presigned PUT
  URL from `initFileUpload`, and the response stores the **full object URL**
  (`https://<endpoint>/<bucket>/<key>`) in `Response.form_data`. `is_valid_s3_url` rejects any URL
  not under the configured endpoint, so after the switch those responses show no files until the
  URLs are rewritten with `manage.py forms_rewrite_file_urls`.

The region matters: Garage rejects SigV4 requests whose credential scope names any region other
than `garage`. Both clients take it from the `AWS_DEFAULT_REGION` env var, which the manifest sets
per environment (`garage` for staging, `us-east-1` for production until this runbook is done).

No bucket CORS is needed: the upload PUT runs inside a Next.js server action, not in the browser.

## Numbers (2026-09-28)

| | objects | size | responses with Minio URLs |
|---|---|---|---|
| production `kompassi` | 3,114 | 2.2 GB | 1,729 of 8,216 |
| staging `kompassidev` | 10 | 105 MB | 7 of 51 |

Read them again before running: `aws s3 ls s3://kompassi/ --recursive --summarize` against Minio
with the `con2` credentials from `~/Hobby/mc-config.json`, and for the responses

```
kubectl -n kompassi-production exec deploy/kompassi -c master -- python manage.py shell -c "
from django.db import connection
with connection.cursor() as c:
    c.execute(\"select count(*) from forms_response where form_data::text like '%minio.con2.fi/kompassi/%'\"); print(c.fetchone())"
```

## Prerequisites

1. **Backup coverage.** `infrastructure/kubernetes/garage-backup.cronjob-sync.yaml` copies only the
   `pictures/` prefix of the edegal site buckets. Add a whole-bucket copy of `kompassi` to it (and
   to the prune job's site loop) before the switch, so the bucket is never without an off-site
   copy. Until then `minio-backup` keeps covering the Minio side.
2. **Capacity.** qb's Garage has 1.1 TiB effective; 2.2 GB is nothing, but check
   `kubectl -n garage exec garage-0 -- /garage status` shows all four nodes healthy.
3. A quiet moment: uploads made between the copy and the switch are caught by the delta sync in
   step 6, but the fewer the better.

## Steps

All `kubectl` commands use the qb kubeconfig. `garage` below means
`kubectl -n garage exec garage-0 -- /garage`.

1. **Bucket and key on Garage.** Same bucket name keeps `MINIO_BUCKET_NAME` unchanged:

   ```
   garage bucket create kompassi
   garage key create kompassi            # note the key ID
   garage bucket allow --read --write --owner kompassi --key kompassi
   garage key info --show-secret kompassi
   ```

2. **Copy the objects.** With 2.2 GB a workstation round trip is fine (`aws s3 sync` cannot talk
   to two endpoints in one command). Use the Minio `con2` credentials for the download and the new
   Garage key for the upload; `AWS_DEFAULT_REGION=garage` for the upload:

   ```
   AWS_ENDPOINT_URL=https://minio.con2.fi aws s3 sync s3://kompassi/ ./kompassi-media
   AWS_ENDPOINT_URL=https://garage.con2.fi aws s3 sync ./kompassi-media s3://kompassi/
   ```

   Then compare `aws s3 ls --recursive` on both sides (size and key per line; sort both listings
   the same way before diffing).

   Staging instead took its copy from piilo's `minio-backup/current/kompassidev/` to exercise the
   backup; that is an option here too, but the live bucket is fresher.

3. **Secret.** Replace the two keys in Secret `kompassi` of `kompassi-production` with the Garage
   key. Running pods keep the old values until they restart, so this is safe to do ahead of the
   deploy:

   ```
   kubectl -n kompassi-production patch secret kompassi -p '{"data":{"minioAccessKeyId":"'"$(printf <key id> | base64)"'","minioSecretAccessKey":"'"$(printf %s <secret> | base64)"'"}}'
   ```

4. **Manifest.** In `kubernetes/manifest.mts`, move `minioEndpointUrl: "https://garage.con2.fi"`
   and `s3Region: "garage"` from the staging override into `base` and drop the Minio values (or
   set them on `production` explicitly). Render both environments to check
   (`ENV=production node --experimental-strip-types manifest.mts` in a scratch dir) and commit.

5. **Deploy.** Push `main`; CI deploys staging automatically and production after the manual gate.
   From the first new pod on, uploads go to Garage and media URLs are presigned against it.

6. **Delta sync.** Objects uploaded to Minio between step 2 and the production rollout: repeat the
   two `aws s3 sync` commands of step 2 once. `sync` only copies new or changed objects.

7. **Rewrite stored form URLs**, dry run first, then apply:

   ```
   kubectl -n kompassi-production exec deploy/kompassi -c master -- python manage.py forms_rewrite_file_urls https://minio.con2.fi/kompassi/
   kubectl -n kompassi-production exec deploy/kompassi -c master -- python manage.py forms_rewrite_file_urls https://minio.con2.fi/kompassi/ --apply
   ```

   The dry-run count should match the responses count from "Numbers" above. The new prefix
   defaults to the configured endpoint and bucket.

8. **Verify.**
   - An event page with a logo and the front-page carousel load images from
     `https://garage.con2.fi/kompassi/...?X-Amz-...` (browser network tab).
   - A survey response that had a file: the file link opens.
   - Submit a test response with a file upload on a survey; the file lands in the Garage bucket
     (`aws s3 ls`) and opens from the response view.
   - Excel export of a survey with file fields still lists the filenames.
   - `kubectl -n kompassi-production logs deploy/kompassi -c master` shows no `botocore` errors.

9. **Afterwards.** Leave the Minio bucket in place for a couple of weeks as a fallback, then delete
   it together with the rest of Minio's decommissioning. Rename the `MINIO_*` variables and
   `minio*` Secret keys to something neutral in a separate change once nothing points at Minio.

## Rollback

Before step 7 has been applied: revert the manifest commit (CI redeploys) and restore the old Secret
values; objects written to Garage in the meantime need copying back with `aws s3 sync` in the other
direction. After step 7: run `forms_rewrite_file_urls https://garage.con2.fi/kompassi/ --new-prefix
https://minio.con2.fi/kompassi/ --apply` as well.
