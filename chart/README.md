# kompassi Helm chart

Deploys Kompassi into one namespace per environment (`kompassi-staging`, `kompassi-production`):

- the Django backend: Deployments `kompassi` (gunicorn, with the `setup` init container),
  `uvicorn` (the tickets_v2 API) and `worker` (the task queue), CronJobs `cron-nightly` and
  `cron-frequent`;
- the V2 frontend: Deployment `frontend` (Next.js);
- a Gateway `kompassi` with an http and an https listener per hostname, HTTPRoutes and Traefik
  Middlewares. cert-manager issues one certificate for all hostnames into Secret
  `ingress-letsencrypt` from the Gateway's `cert-manager.io/cluster-issuer` annotation.

`.github/workflows/cicd.yaml` builds `ghcr.io/con2/kompassi` and `ghcr.io/con2/kompassi2` with the
commit SHA as the tag and runs `helm upgrade --install kompassi chart` into staging, then after a
manual gate into production, on every push to main.

```sh
helm lint chart -f chart/values-staging.yaml
helm template kompassi chart -f chart/values-staging.yaml
```

## Prerequisites per namespace

Three Secrets, managed out of band:

- `kompassi`: `secretKey`, `ticketsApiKey`, `desuprofileOauth2ClientId`,
  `desuprofileOauth2ClientSecret`, `s3AccessKeyId`, `s3SecretAccessKey`, `oidcRsaPrivateKey`,
  `sshPrivateKey`, `sshKnownHosts`.
- `postgres`: `hostname`, `database`, `username`, `password`. For a database on the shared
  CloudNativePG cluster, `infrastructure/kubernetes/postgres/update-secret.sh` writes this shape.
- `kompassi2`: `NEXTAUTH_SECRET`, `KOMPASSI_OIDC_CLIENT_ID`, `KOMPASSI_OIDC_CLIENT_SECRET`,
  `KOMPASSI_TICKETS_V2_API_KEY`. The last one must equal `ticketsApiKey` in `kompassi`.

The Kompassi OIDC client used by the frontend must allow the redirect URI
`https://<frontend hostname>/api/auth/callback/kompassi`.

## Field ownership after the adoption from kubectl

The backend objects were adopted from kubectl-applied manifests. Helm installs with server-side
apply, and a field that Helm has not changed since the adoption is still owned by the placeholder
`before-first-apply`. The first deploy that changes such a field fails with
`Apply failed with 1 conflict: conflict with "before-first-apply"`. Deploy that one change by hand
with `--force-conflicts` (the CI command from `.github/workflows/cicd.yaml` plus the flag); Helm
then owns the field and later deploys need nothing special.

Server-side apply also never removes a list item another manager still owns. The cron job
containers therefore keep the unused `containerPort: 8000` from the old manifests after the chart
drops it.

## One-time cutover from skaffold

Until this cutover, the frontend lived in its own namespace (`kompassi2-<env>`) with its own
Gateway, and both components were deployed with skaffold. Do this by hand once per environment,
staging first, before merging the switch to `cicd.yaml`. `<env>` is `staging` or `production`.

1. Copy the frontend Secret into the backend namespace:

   ```sh
   kubectl -n kompassi2-<env> get secret kompassi2 -o json \
     | jq 'del(.metadata.namespace, .metadata.uid, .metadata.resourceVersion, .metadata.creationTimestamp, .metadata.managedFields, .metadata.ownerReferences)' \
     | kubectl -n kompassi-<env> apply -f -
   ```

2. Mark the existing backend objects as belonging to the release:

   ```sh
   for object in deployment/kompassi deployment/uvicorn deployment/worker \
       service/kompassi service/uvicorn cronjob/cron-nightly cronjob/cron-frequent \
       gateway.gateway.networking.k8s.io/kompassi \
       httproute.gateway.networking.k8s.io/redirect-https httproute.gateway.networking.k8s.io/kompassi \
       middleware.traefik.io/body-100m middleware.traefik.io/retry; do
     kubectl -n kompassi-<env> label "$object" app.kubernetes.io/managed-by=Helm
     kubectl -n kompassi-<env> annotate "$object" meta.helm.sh/release-name=kompassi \
       meta.helm.sh/release-namespace=kompassi-<env>
   done
   ```

3. Read the diff against the live objects. Expect only the frontend objects, the v2 listeners,
   labels, resource requests, security context hardening and the shorter
   `KOMPASSI_TICKETS_V2_API_URL`:

   ```sh
   helm template kompassi chart -f chart/values-<env>.yaml --set image.tag=<deployed sha> \
     | kubectl -n kompassi-<env> diff --server-side --force-conflicts -f -
   ```

4. Install with the image tag currently deployed:

   ```sh
   helm upgrade --install kompassi chart --namespace kompassi-<env> \
     -f chart/values-<env>.yaml --set image.tag=<deployed sha> \
     --wait --timeout 600s --force-conflicts
   ```

   Check that all pods are Ready and that the frontend answers inside the namespace:
   `kubectl -n kompassi-<env> run curl --rm -it --restart=Never --image=curlimages/curl -- curl -sI -H 'Host: <frontend hostname>' http://frontend:3000/healthz`.

5. cert-manager now re-issues `ingress-letsencrypt` with the frontend hostname added. Until then
   the old `kompassi2` Gateway in `kompassi2-<env>` keeps serving the frontend hostname with its
   own certificate; both routes point at working pods. Once
   `kubectl -n kompassi-<env> get certificate ingress-letsencrypt -o jsonpath='{.spec.dnsNames}'`
   lists the frontend hostname and the Certificate is Ready, delete the old routing:

   ```sh
   kubectl -n kompassi2-<env> delete httproute kompassi2 redirect-https
   kubectl -n kompassi2-<env> delete gateway kompassi2
   ```

   After a day without errors, `kubectl delete namespace kompassi2-<env>`.

6. Merge the switch to `cicd.yaml`. Its first deploy needs no `--force-conflicts`, since step 4
   already took over the fields.

The hostnames do not change, so neither DNS nor the OIDC redirect URIs need updating.
