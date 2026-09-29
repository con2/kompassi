{{- define "kompassi.labels" -}}
stack: kompassi
{{- end -}}

{{- define "kompassi.backendSecretName" -}}
{{ .Values.backend.existingSecretName | default "kompassi" }}
{{- end -}}

{{- define "kompassi.postgresSecretName" -}}
{{ .Values.backend.existingPostgresSecretName | default "postgres" }}
{{- end -}}

{{- define "kompassi.frontendSecretName" -}}
{{ .Values.frontend.existingSecretName | default "kompassi2" }}
{{- end -}}

{{/* The Secret the old Ingress used, so the Gateway reuses its certificate instead of reissuing. */}}
{{- define "kompassi.tlsSecretName" -}}
ingress-letsencrypt
{{- end -}}

{{- define "kompassi.backendImage" -}}
{{ .Values.backend.image.repository }}:{{ .Values.image.tag }}
{{- end -}}

{{- define "kompassi.primaryHostname" -}}
{{ first .Values.backend.hostnames }}
{{- end -}}

{{/* Listener name on the Gateway. Takes a list: protocol ("http" or "https"), hostname. */}}
{{- define "kompassi.listenerName" -}}
{{ index . 0 }}-{{ index . 1 | replace "." "-" }}
{{- end -}}

{{- define "kompassi.podSecurityContext" -}}
runAsUser: 998
runAsGroup: 998
fsGroup: 998
runAsNonRoot: true
seccompProfile:
  type: RuntimeDefault
{{- end -}}

{{- define "kompassi.containerSecurityContext" -}}
readOnlyRootFilesystem: true
allowPrivilegeEscalation: false
capabilities:
  drop: [ALL]
{{- end -}}

{{/*
Prefers spreading pods across nodes, away from pods whose `component` label is the argument. The
cron jobs pass "kompassi", not their own component, so they spread away from the gunicorn pods.
*/}}
{{- define "kompassi.podAntiAffinity" -}}
podAntiAffinity:
  preferredDuringSchedulingIgnoredDuringExecution:
    - weight: 50
      podAffinityTerm:
        labelSelector:
          matchExpressions:
            - key: component
              operator: In
              values: [{{ . | quote }}]
        topologyKey: kubernetes.io/hostname
{{- end -}}

{{/*
Roll one pod at a time and never below the current count. The old pod keeps serving through the
preStop sleep because endpoint removal and SIGTERM start at the same instant, and Traefik needs a
few seconds (its 2 s provider throttle plus API propagation) to stop routing to the pod. Gunicorn,
uvicorn and Next.js stop accepting connections immediately on SIGTERM, so without the sleep every
rollout returned 502s for that window. The three helpers below go together on every Deployment
behind the Gateway.
*/}}
{{- define "kompassi.rollout" -}}
type: RollingUpdate
rollingUpdate:
  maxSurge: 1
  maxUnavailable: 0
{{- end -}}

{{/* Leaves the server's own 30 s graceful timeout intact after the preStop sleep. */}}
{{- define "kompassi.terminationGracePeriodSeconds" -}}
{{ add .Values.preStopSleepSeconds 35 }}
{{- end -}}

{{- define "kompassi.preStop" -}}
preStop:
  sleep:
    seconds: {{ .Values.preStopSleepSeconds }}
{{- end -}}

{{/*
Backend env vars are listed inline instead of coming from a ConfigMap. The Deployments were adopted
from kubectl-applied manifests that had them inline, and server-side apply never removes list items
another field manager owns, so those stale entries would shadow a ConfigMap forever.
*/}}
{{- define "kompassi.backendEnv" -}}
{{- $secret := include "kompassi.backendSecretName" . -}}
{{- $postgres := include "kompassi.postgresSecretName" . -}}
- name: POSTGRES_HOSTNAME
  valueFrom: { secretKeyRef: { name: {{ $postgres }}, key: hostname } }
- name: POSTGRES_DATABASE
  valueFrom: { secretKeyRef: { name: {{ $postgres }}, key: database } }
- name: POSTGRES_USERNAME
  valueFrom: { secretKeyRef: { name: {{ $postgres }}, key: username } }
- name: POSTGRES_PASSWORD
  valueFrom: { secretKeyRef: { name: {{ $postgres }}, key: password } }
- name: POSTGRES_SSLMODE
  value: {{ .Values.backend.postgresSslMode | quote }}
- name: REDIS_HOSTNAME
  value: {{ .Values.backend.redis.hostname | quote }}
- name: REDIS_CACHE_DATABASE
  value: {{ .Values.backend.redis.cacheDatabase | quote }}
- name: SECRET_KEY
  valueFrom: { secretKeyRef: { name: {{ $secret }}, key: secretKey } }
- name: ALLOWED_HOSTS
  value: {{ join " " .Values.backend.hostnames | quote }}
- name: EMAIL_HOST
  value: {{ .Values.backend.mail.smtpServer | quote }}
- name: DEFAULT_FROM_EMAIL
  value: {{ .Values.backend.mail.defaultFromEmail | quote }}
- name: ADMINS
  value: {{ join "," .Values.backend.admins | quote }}
- name: KOMPASSI_INSTALLATION_NAME
  value: {{ .Values.backend.installationName | quote }}
- name: KOMPASSI_INSTALLATION_SLUG
  value: {{ .Values.backend.installationSlug | quote }}
- name: KOMPASSI_BASE_URL
  value: {{ .Values.backend.baseUrl | quote }}
- name: KOMPASSI_V2_BASE_URL
  value: {{ printf "https://%s" .Values.frontend.hostname | quote }}
- name: KOMPASSI_TICKETS_V2_API_URL
  value: http://uvicorn:7998
- name: KOMPASSI_TICKETS_V2_API_KEY
  valueFrom: { secretKeyRef: { name: {{ $secret }}, key: ticketsApiKey } }
- name: KOMPASSI_DESUPROFILE_OAUTH2_CLIENT_ID
  valueFrom: { secretKeyRef: { name: {{ $secret }}, key: desuprofileOauth2ClientId } }
- name: KOMPASSI_DESUPROFILE_OAUTH2_CLIENT_SECRET
  valueFrom: { secretKeyRef: { name: {{ $secret }}, key: desuprofileOauth2ClientSecret } }
- name: KOMPASSI_CSP_ALLOWED_LOGIN_REDIRECTS
  value: {{ join " " .Values.backend.allowedLoginRedirects | quote }}
# `manage.py setup` does nothing when the run ID has not changed since its last run.
- name: KOMPASSI_SETUP_RUN_ID
  valueFrom: { fieldRef: { fieldPath: "metadata.labels['pod-template-hash']" } }
- name: S3_BUCKET_NAME
  value: {{ .Values.backend.s3.bucketName | quote }}
- name: S3_ACCESS_KEY_ID
  valueFrom: { secretKeyRef: { name: {{ $secret }}, key: s3AccessKeyId } }
- name: S3_SECRET_ACCESS_KEY
  valueFrom: { secretKeyRef: { name: {{ $secret }}, key: s3SecretAccessKey } }
- name: S3_ENDPOINT_URL
  value: {{ .Values.backend.s3.endpointUrl | quote }}
# Read by every boto3 client in the app (django-storages and forms/utils/s3_presign.py).
- name: AWS_DEFAULT_REGION
  value: {{ .Values.backend.s3.region | quote }}
- name: OIDC_RSA_PRIVATE_KEY
  valueFrom: { secretKeyRef: { name: {{ $secret }}, key: oidcRsaPrivateKey } }
- name: XDG_CACHE_HOME
  value: /tmp
{{- end -}}

{{- define "kompassi.backendVolumeMounts" -}}
- name: kompassi-media
  mountPath: /usr/src/app/media
- name: kompassi-temp
  mountPath: /tmp
- name: kompassi-secret
  mountPath: /mnt/secrets/kompassi
{{- end -}}

{{- define "kompassi.backendVolumes" -}}
- name: kompassi-secret
  secret:
    secretName: {{ include "kompassi.backendSecretName" . }}
    items:
      - key: sshPrivateKey
        path: sshPrivateKey
      - key: sshKnownHosts
        path: sshKnownHosts
- name: kompassi-temp
  emptyDir: {}
# Media is stored in S3; the directory only has to be writable.
- name: kompassi-media
  emptyDir: {}
{{- end -}}

{{/* A probe hitting `path` on `port` of the pod. Takes a list: path, port, Host header. */}}
{{- define "kompassi.httpGet" -}}
httpGet:
  path: {{ index . 0 }}
  port: {{ index . 1 }}
  httpHeaders:
    - name: Host
      value: {{ index . 2 | quote }}
{{- end -}}
