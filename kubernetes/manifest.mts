// Generate Kubernetes manifests based on environment variables.
// See https://github.com/japsu/depleten for philosophy, and
// kompassi-v2-frontend/kubernetes/manifest.ts for a smaller sibling example.
// Usage: ENV=staging node --experimental-strip-types manifest.mts
// (intended to be run with this file's own directory as the cwd)

import { existsSync, mkdirSync, readdirSync, unlinkSync, writeFileSync } from "fs";
import path from "path";

interface Environment {
  ingressPublicHostnames: string[];
  backupIngressPublicHostnames: string[];

  kompassiSecretManaged: boolean;
  kompassiStoragePvc: boolean;
  kompassiStoragePvcStorageClass: string | undefined;
  kompassiStorageNfs: string;
  kompassiStorageNfsPath: string;
  kompassiInstallationSlug: string;
  kompassiInstallationName: string;
  kompassiBaseUrl: string;
  kompassiV2BaseUrl: string;
  kompassiTicketsV2ApiUrl: string;
  kompassiCorsAllowedHosts: string[];
  kompassiCspAllowedLoginRedirects: string[];
  kompassiAdmins: string[];
  kompassiWorkers: number;
  kompassiTimeoutSeconds: number;
  kompassiCronNightlyEnabled: boolean;
  kompassiCronNightlySuspended: boolean;
  kompassiUvicornEnabled: boolean;
  kompassiBackgroundWorkerEnabled: boolean;
  kompassiReadinessProbeEnabled: boolean;
  kompassiLivenessProbeEnabled: boolean;

  // only used when kompassiSecretManaged is true (local dev)
  kompassiSecretKey: string;
  minioAccessKeyId: string;
  minioSecretAccessKey: string;

  postgresManaged: boolean;
  postgresHostname: string;
  postgresDatabase: string;
  postgresUsername: string;
  // only used when postgresManaged is true (local dev); empty means autogenerate
  postgresPassword: string;
  postgresSsl: boolean;
  // shared with redis's PVC below -- see comment on redisStoragePvcStorageClass
  postgresStoragePvcStorageClass: string | undefined;

  redisManaged: boolean;
  redisHostname: string;
  redisBrokerDatabase: number;
  redisCacheDatabase: number;
  redisStoragePvc: boolean;

  minioBucketName: string;
  minioEndpointUrl: string;

  smtpServer: string;
  smtpDefaultFromEmail: string;

  setupShouldRun: boolean;

  ingressLetsencryptEnabled: boolean;
}

type EnvironmentName = "dev" | "staging" | "production";
const environmentNames: EnvironmentName[] = ["dev", "staging", "production"];

// Shared defaults, overridden per environment below. Roughly corresponds to
// the old kubernetes/default.vars.yaml.
const base: Environment = {
  ingressPublicHostnames: ["kompassi.localhost"],
  backupIngressPublicHostnames: [],

  kompassiSecretManaged: true,
  kompassiStoragePvc: true,
  kompassiStoragePvcStorageClass: undefined,
  kompassiStorageNfs: "",
  kompassiStorageNfsPath: "/",
  kompassiInstallationSlug: "komplocaldev",
  kompassiInstallationName: "Kompassi (LOCAL DEV)",
  kompassiBaseUrl: "http://kompassi.localhost",
  kompassiV2BaseUrl: "http://kompassi2.localhost",
  kompassiTicketsV2ApiUrl: "http://uvicorn.default.svc.cluster.local:7998",
  kompassiCorsAllowedHosts: [],
  kompassiCspAllowedLoginRedirects: [],
  kompassiAdmins: [],
  kompassiWorkers: 4,
  kompassiTimeoutSeconds: 120,
  kompassiCronNightlyEnabled: true,
  kompassiCronNightlySuspended: false,
  kompassiUvicornEnabled: true,
  kompassiBackgroundWorkerEnabled: true,
  kompassiReadinessProbeEnabled: true,
  kompassiLivenessProbeEnabled: true,

  kompassiSecretKey: "not a very secret key",
  minioAccessKeyId: "kompassi",
  minioSecretAccessKey: "kompassi",

  postgresManaged: true,
  postgresHostname: "postgres",
  postgresDatabase: "kompassi",
  postgresUsername: "kompassi",
  postgresPassword: "knownpassword",
  postgresSsl: false,
  postgresStoragePvcStorageClass: undefined,

  redisManaged: true,
  redisHostname: "redis",
  redisBrokerDatabase: 1,
  redisCacheDatabase: 2,
  redisStoragePvc: true,

  minioBucketName: "kompassi",
  minioEndpointUrl: "http://minio:9000",

  smtpServer: "",
  smtpDefaultFromEmail: "",

  setupShouldRun: true,

  ingressLetsencryptEnabled: false,
};

const environmentOverrides: Record<EnvironmentName, Partial<Environment>> = {
  dev: {},
  staging: {
    ingressPublicHostnames: ["dev.kompassi.eu"],

    postgresManaged: false,
    postgresHostname: "siilo.tracon.fi",
    postgresDatabase: "kompassidev",
    postgresUsername: "kompassidev",
    postgresSsl: true,

    redisManaged: false,
    redisHostname: "redis-ha-haproxy.redis-ha.svc.cluster.local",
    redisBrokerDatabase: 7,
    redisCacheDatabase: 7,

    kompassiSecretManaged: false,
    kompassiStoragePvc: false,
    kompassiStoragePvcStorageClass: "longhorn-nfs",
    kompassiInstallationName: "Kompassi (DEV)",
    kompassiInstallationSlug: "turskadev",
    kompassiBaseUrl: "https://dev.kompassi.eu",
    kompassiV2BaseUrl: "https://v2.dev.kompassi.eu",
    kompassiTicketsV2ApiUrl:
      "http://uvicorn.kompassi-staging.svc.cluster.local:7998",
    kompassiAdmins: ["Luka Pajukanta <santtu@pajukanta.fi>"],
    kompassiCspAllowedLoginRedirects: [
      "dev.ropekonsti.fi",
      "http://localhost:3000",
      "https://localhost:3000",
      "http://localhost:5000",
      "https://localhost:5000",
      "http://localhost:8000",
      "https://localhost:8000",
      "ropekonsti.fi",
      "wp.ropecon.fi",
      "dev.larpit.fi",
    ],
    kompassiWorkers: 8,

    smtpServer: "sr1.pahaip.fi",
    smtpDefaultFromEmail: "suunnistajat@kompassi.eu",

    ingressLetsencryptEnabled: true,

    minioBucketName: "kompassidev",
    minioEndpointUrl: "https://minio.con2.fi",
  },
  production: {
    ingressPublicHostnames: ["kompassi.eu", "conit.fi"],
    backupIngressPublicHostnames: ["vara.kompassi.eu"],

    postgresManaged: false,
    postgresHostname: "siilo.tracon.fi",
    postgresDatabase: "kompassi",
    postgresUsername: "kompassi",
    postgresSsl: true,

    redisManaged: false,
    redisHostname: "redis-ha-haproxy.redis-ha.svc.cluster.local",
    redisBrokerDatabase: 9,
    redisCacheDatabase: 9,

    kompassiSecretManaged: false,
    kompassiStoragePvc: false,
    kompassiStoragePvcStorageClass: "longhorn-nfs",
    kompassiInstallationName: "Kompassi",
    kompassiInstallationSlug: "turska",
    kompassiBaseUrl: "https://kompassi.eu",
    kompassiV2BaseUrl: "https://v2.kompassi.eu",
    kompassiTicketsV2ApiUrl:
      "http://uvicorn.kompassi-production.svc.cluster.local:7998",
    kompassiAdmins: ["Luka Pajukanta <santtu@pajukanta.fi>"],
    kompassiCorsAllowedHosts: [],
    // TODO this list should probably be autogenerated from the list of Kompassi OIDC clients
    // https://kompassi.eu/admin/oauth2_provider/application/
    kompassiCspAllowedLoginRedirects: [
      "*.tracon.fi",
      "*.con2.fi",
      "*.ropecon.fi",
      "*.kompassi.eu",
      "*.solmukohta.eu",
      "*.kotae.fi",
      "conikuvat.fi",
      "larppikuvat.fi",
      "ropekonsti.fi",
      "larpit.fi",
    ],
    kompassiWorkers: 12,
    kompassiReadinessProbeEnabled: false,
    kompassiLivenessProbeEnabled: false,

    smtpServer: "sr1.pahaip.fi",
    smtpDefaultFromEmail: "suunnistajat@kompassi.eu",

    ingressLetsencryptEnabled: true,

    minioBucketName: "kompassi",
    minioEndpointUrl: "https://minio.con2.fi",
  },
};

function getEnvironmentName(): EnvironmentName {
  const environmentName = process.env.ENV;
  if (!environmentNames.includes(environmentName as EnvironmentName)) {
    return "dev";
  }
  return environmentName as EnvironmentName;
}

const environmentName = getEnvironmentName();
const env: Environment = { ...base, ...environmentOverrides[environmentName] };

// --- Constants that don't vary by environment ---

export const stack = "kompassi";
const kompassiImage = "kompassi"; // image name/tag managed by skaffold
const kompassiStaticImage = "kompassi-static";
const ingressClassName = "traefik";
const clusterIssuer = "letsencrypt-prod";

const kompassiPodSecurityContext = {
  runAsUser: 998,
  runAsGroup: 998,
  fsGroup: 998,
};
const kompassiContainerSecurityContext = {
  readOnlyRootFilesystem: true,
  allowPrivilegeEscalation: false,
};

const primaryHostname = env.ingressPublicHostnames[0];
const kompassiAllowedHosts = [
  ...env.ingressPublicHostnames,
  ...env.backupIngressPublicHostnames,
];

export function labels(component?: string) {
  return { stack, component };
}

function secretKeyRef(name: string, key: string) {
  return { secretKeyRef: { name, key } };
}

export function b64(str: string) {
  return Buffer.from(str).toString("base64");
}

// Anti-affinity: prefer spreading pods of the same component across nodes.
// componentName is the `component` label to spread apart -- for the nightly
// cron job this is (perhaps a little surprisingly, but faithfully preserved
// from the original Emrichen template) "kompassi", not "cron-nightly".
function podAffinity(componentName: string) {
  return {
    podAntiAffinity: {
      preferredDuringSchedulingIgnoredDuringExecution: [
        {
          weight: 50,
          podAffinityTerm: {
            labelSelector: {
              matchExpressions: [
                { key: "component", operator: "In", values: [componentName] },
              ],
            },
            topologyKey: "kubernetes.io/hostname",
          },
        },
      ],
    },
  };
}

// Common environment variables for the kompassi, celery, worker, uvicorn and
// cron-nightly pods.
const kompassiEnvironment = Object.entries({
  POSTGRES_HOSTNAME: secretKeyRef("postgres", "hostname"),
  POSTGRES_DATABASE: secretKeyRef("postgres", "database"),
  POSTGRES_USERNAME: secretKeyRef("postgres", "username"),
  POSTGRES_PASSWORD: secretKeyRef("postgres", "password"),
  POSTGRES_SSLMODE: env.postgresSsl ? "require" : "allow",
  REDIS_HOSTNAME: env.redisHostname,
  REDIS_BROKER_DATABASE: String(env.redisBrokerDatabase),
  REDIS_CACHE_DATABASE: String(env.redisCacheDatabase),
  SECRET_KEY: secretKeyRef("kompassi", "secretKey"),
  ALLOWED_HOSTS: kompassiAllowedHosts.join(" "),
  EMAIL_HOST: env.smtpServer,
  DEFAULT_FROM_EMAIL: env.smtpDefaultFromEmail,
  ADMINS: env.kompassiAdmins.join(","),
  KOMPASSI_INSTALLATION_NAME: env.kompassiInstallationName,
  KOMPASSI_INSTALLATION_SLUG: env.kompassiInstallationSlug,
  KOMPASSI_BASE_URL: env.kompassiBaseUrl,
  KOMPASSI_V2_BASE_URL: env.kompassiV2BaseUrl,
  KOMPASSI_TICKETS_V2_API_URL: env.kompassiTicketsV2ApiUrl,
  // NOTE: was "ticketsApikey" (lowercase k) on the Secret side under Emrichen,
  // which never actually matched this env var's "ticketsApiKey" -- fixed here.
  KOMPASSI_TICKETS_V2_API_KEY: secretKeyRef("kompassi", "ticketsApiKey"),
  KOMPASSI_DESUPROFILE_OAUTH2_CLIENT_ID: secretKeyRef(
    "kompassi",
    "desuprofileOauth2ClientId",
  ),
  KOMPASSI_DESUPROFILE_OAUTH2_CLIENT_SECRET: secretKeyRef(
    "kompassi",
    "desuprofileOauth2ClientSecret",
  ),
  CORS_ORIGIN_WHITELIST: env.kompassiCorsAllowedHosts.join(" "),
  KOMPASSI_CSP_ALLOWED_LOGIN_REDIRECTS:
    env.kompassiCspAllowedLoginRedirects.join(" "),
  // used by `manage.py setup` to do nothing if nothing has changed
  KOMPASSI_SETUP_RUN_ID: {
    fieldRef: { fieldPath: "metadata.labels['pod-template-hash']" },
  },
  MINIO_BUCKET_NAME: env.minioBucketName,
  MINIO_ACCESS_KEY_ID: secretKeyRef("kompassi", "minioAccessKeyId"),
  MINIO_SECRET_ACCESS_KEY: secretKeyRef("kompassi", "minioSecretAccessKey"),
  MINIO_ENDPOINT_URL: env.minioEndpointUrl,
  OIDC_RSA_PRIVATE_KEY: secretKeyRef("kompassi", "oidcRsaPrivateKey"),
  XDG_CACHE_HOME: "/tmp",
}).map(([name, value]) =>
  value instanceof Object ? { name, valueFrom: value } : { name, value: String(value) },
);

const kompassiVolumeMounts = [
  { mountPath: "/usr/src/app/media", name: "kompassi-media" },
  { mountPath: "/tmp", name: "kompassi-temp" },
  { mountPath: "/mnt/secrets/kompassi", name: "kompassi-secret" },
];

function kompassiMediaVolume() {
  if (env.kompassiStoragePvc) {
    return {
      name: "kompassi-media",
      persistentVolumeClaim: { claimName: "kompassi-media" },
    };
  }
  if (env.kompassiStorageNfs) {
    return {
      name: "kompassi-media",
      nfs: { server: env.kompassiStorageNfs, path: env.kompassiStorageNfsPath },
    };
  }
  return { name: "kompassi-media", emptyDir: {} };
}

const kompassiVolumes = [
  {
    name: "kompassi-secret",
    secret: {
      secretName: "kompassi",
      items: [
        { key: "sshPrivateKey", path: "sshPrivateKey" },
        { key: "sshKnownHosts", path: "sshKnownHosts" },
      ],
    },
  },
  { name: "kompassi-temp", emptyDir: {} },
  kompassiMediaVolume(),
];

function kompassiProbe(path: string, port: number) {
  return {
    httpGet: {
      path,
      port,
      httpHeaders: [{ name: "Host", value: primaryHostname }],
    },
  };
}

// --- REDIS ---

const redisService = {
  apiVersion: "v1",
  kind: "Service",
  metadata: { name: "redis", labels: labels("redis") },
  spec: {
    ports: [{ port: 6379, targetPort: 6379 }],
    selector: labels("redis"),
  },
};

const redisDeployment = {
  apiVersion: "apps/v1",
  kind: "Deployment",
  metadata: { name: "redis" },
  spec: {
    selector: { matchLabels: labels("redis") },
    template: {
      metadata: { labels: labels("redis") },
      spec: {
        enableServiceLinks: false,
        containers: [
          {
            name: "master",
            image: "redis",
            args: ["redis-server", "--appendonly", "yes"],
            ports: [{ containerPort: 6379 }],
            volumeMounts: [{ mountPath: "/data", name: "redis-data" }],
          },
        ],
        volumes: [
          {
            name: "redis-data",
            persistentVolumeClaim: { claimName: "redis-data" },
          },
        ],
      },
    },
  },
};

const redisPvc = {
  apiVersion: "v1",
  kind: "PersistentVolumeClaim",
  metadata: { labels: labels("redis"), name: "redis-data" },
  spec: {
    // NOTE: reuses postgresStoragePvcStorageClass, matching the original
    // Emrichen template's kubernetes/redis/pvc.in.yaml -- there is no
    // separate redis storage class in practice, only ever exercised in dev.
    storageClassName: env.postgresStoragePvcStorageClass,
    accessModes: ["ReadWriteOnce"],
    resources: { requests: { storage: "1000Mi" } },
  },
};

// --- POSTGRESQL ---

const postgresService = {
  apiVersion: "v1",
  kind: "Service",
  metadata: { name: "postgres", labels: labels("postgres") },
  spec: {
    ports: [{ port: 5432, targetPort: 5432 }],
    selector: labels("postgres"),
  },
};

const postgresDeployment = {
  apiVersion: "apps/v1",
  kind: "Deployment",
  metadata: { name: "postgres" },
  spec: {
    selector: { matchLabels: labels("postgres") },
    template: {
      metadata: { labels: labels("postgres") },
      spec: {
        enableServiceLinks: false,
        containers: [
          {
            name: "master",
            image: "postgres",
            ports: [{ containerPort: 5432 }],
            env: [
              { name: "POSTGRES_DB", value: env.postgresDatabase },
              {
                name: "POSTGRES_USER",
                valueFrom: secretKeyRef("postgres", "username"),
              },
              {
                name: "POSTGRES_PASSWORD",
                valueFrom: secretKeyRef("postgres", "password"),
              },
            ],
            volumeMounts: [
              { mountPath: "/var/lib/postgresql", name: "postgres-data" },
            ],
            readinessProbe: {
              exec: { command: ["pg_isready", "-U", "kompassi"] },
              initialDelaySeconds: 15,
              periodSeconds: 30,
            },
            livenessProbe: {
              exec: { command: ["pg_isready", "-U", "kompassi"] },
              initialDelaySeconds: 30,
              periodSeconds: 30,
            },
          },
        ],
        volumes: [
          {
            name: "postgres-data",
            persistentVolumeClaim: { claimName: "postgres-data" },
          },
        ],
      },
    },
  },
};

const postgresPvc = {
  apiVersion: "v1",
  kind: "PersistentVolumeClaim",
  metadata: { labels: labels("postgres"), name: "postgres-data" },
  spec: {
    storageClassName: env.postgresStoragePvcStorageClass,
    accessModes: ["ReadWriteOnce"],
    resources: { requests: { storage: "1000Mi" } },
  },
};

const postgresSecret = {
  apiVersion: "v1",
  kind: "Secret",
  metadata: {
    name: "postgres",
    labels: labels("postgres"),
    annotations: env.postgresPassword
      ? undefined
      : { "secret-generator.v1.mittwald.de/autogenerate": "password" },
  },
  type: "Opaque",
  data: {
    username: b64(env.postgresUsername),
    hostname: b64(env.postgresHostname),
    database: b64(env.postgresDatabase),
    password: env.postgresPassword ? b64(env.postgresPassword) : undefined,
  },
};

// --- GUNICORN (kompassi web server) ---

const kompassiService = {
  apiVersion: "v1",
  kind: "Service",
  metadata: { name: "kompassi", labels: labels("kompassi") },
  spec: {
    ports: [{ port: 8000, targetPort: 8000 }],
    selector: labels("kompassi"),
  },
};

const kompassiDeployment = {
  apiVersion: "apps/v1",
  kind: "Deployment",
  metadata: { name: "kompassi" },
  spec: {
    selector: { matchLabels: labels("kompassi") },
    template: {
      metadata: { labels: labels("kompassi") },
      spec: {
        affinity: podAffinity("kompassi"),
        enableServiceLinks: false,
        securityContext: kompassiPodSecurityContext,
        initContainers: env.setupShouldRun
          ? [
              {
                name: "setup",
                image: kompassiImage,
                args: ["python", "manage.py", "setup"],
                env: kompassiEnvironment,
                securityContext: kompassiContainerSecurityContext,
              },
            ]
          : [],
        containers: [
          {
            name: "master",
            image: kompassiImage,
            ports: [{ containerPort: 8000 }],
            env: kompassiEnvironment,
            securityContext: kompassiContainerSecurityContext,
            args: [
              "gunicorn",
              `--workers=${env.kompassiWorkers}`,
              "--bind=0.0.0.0:8000",
              "--capture-output",
              `--timeout=${env.kompassiTimeoutSeconds}`,
              "kompassi.wsgi",
            ],
            startupProbe: kompassiProbe("/api/v1/status", 8000),
            readinessProbe: env.kompassiReadinessProbeEnabled
              ? { ...kompassiProbe("/api/v1/status", 8000), periodSeconds: 30 }
              : undefined,
            livenessProbe: env.kompassiLivenessProbeEnabled
              ? {
                  ...kompassiProbe("/api/v1/status", 8000),
                  initialDelaySeconds: 15,
                  periodSeconds: 30,
                }
              : undefined,
            volumeMounts: kompassiVolumeMounts,
          },
        ],
        volumes: kompassiVolumes,
      },
    },
  },
};

const kompassiPvc = {
  apiVersion: "v1",
  kind: "PersistentVolumeClaim",
  metadata: { labels: labels("kompassi"), name: "kompassi-media" },
  spec: {
    storageClassName: env.kompassiStoragePvcStorageClass,
    accessModes: ["ReadWriteMany"],
    resources: { requests: { storage: "1000Mi" } },
  },
};

const kompassiSecret = {
  apiVersion: "v1",
  kind: "Secret",
  metadata: { name: "kompassi", labels: { stack } },
  type: "Opaque",
  data: {
    desuprofileOauth2ClientId: "",
    desuprofileOauth2ClientSecret: "",
    sshPrivateKey: b64("bogus"),
    sshKnownHosts: b64("bogus"),
    secretKey: b64(env.kompassiSecretKey),
    minioAccessKeyId: b64(env.minioAccessKeyId),
    minioSecretAccessKey: b64(env.minioSecretAccessKey),
    oidcRsaPrivateKey: "",
    ticketsApiKey: b64("secret"),
  },
};

// --- UVICORN (optimized server for tickets_v2) ---

const uvicornService = {
  apiVersion: "v1",
  kind: "Service",
  metadata: { name: "uvicorn", labels: labels("uvicorn") },
  spec: {
    ports: [{ port: 7998, targetPort: 7998 }],
    selector: labels("uvicorn"),
  },
};

const uvicornDeployment = {
  apiVersion: "apps/v1",
  kind: "Deployment",
  metadata: { name: "uvicorn" },
  spec: {
    selector: { matchLabels: labels("uvicorn") },
    template: {
      metadata: { labels: labels("uvicorn") },
      spec: {
        affinity: podAffinity("uvicorn"),
        enableServiceLinks: false,
        securityContext: kompassiPodSecurityContext,
        containers: [
          {
            name: "master",
            image: kompassiImage,
            ports: [{ containerPort: 7998 }],
            env: kompassiEnvironment,
            securityContext: kompassiContainerSecurityContext,
            args: [
              "uvicorn",
              "--host=0.0.0.0",
              "--port=7998",
              "--no-access-log",
              `--workers=${env.kompassiWorkers}`,
              "kompassi.tickets_v2.optimized_server.app:app",
            ],
            startupProbe: kompassiProbe("/api/tickets-v2/status", 7998),
            readinessProbe: {
              ...kompassiProbe("/api/tickets-v2/status", 7998),
              periodSeconds: 30,
            },
            livenessProbe: {
              ...kompassiProbe("/api/tickets-v2/status", 7998),
              initialDelaySeconds: 15,
              periodSeconds: 30,
            },
          },
        ],
      },
    },
  },
};

// --- CRON (scheduled tasks) ---

const cronNightly = {
  apiVersion: "batch/v1",
  kind: "CronJob",
  metadata: { name: "cron-nightly" },
  spec: {
    schedule: "7 0 * * *",
    successfulJobsHistoryLimit: 1,
    failedJobsHistoryLimit: 3,
    concurrencyPolicy: "Forbid",
    suspend: env.kompassiCronNightlySuspended,
    jobTemplate: {
      spec: {
        template: {
          metadata: { labels: labels("cron-nightly") },
          spec: {
            affinity: podAffinity("kompassi"),
            enableServiceLinks: false,
            securityContext: kompassiPodSecurityContext,
            restartPolicy: "OnFailure",
            containers: [
              {
                name: "master",
                image: kompassiImage,
                ports: [{ containerPort: 8000 }],
                env: kompassiEnvironment,
                securityContext: kompassiContainerSecurityContext,
                args: ["python", "manage.py", "cron_nightly"],
                volumeMounts: kompassiVolumeMounts,
              },
            ],
            volumes: kompassiVolumes,
          },
        },
      },
    },
  },
};

// --- CELERY (background worker) ---

const celeryDeployment = {
  apiVersion: "apps/v1",
  kind: "Deployment",
  metadata: { name: "celery" },
  spec: {
    selector: { matchLabels: labels("celery") },
    template: {
      metadata: { labels: labels("celery") },
      spec: {
        affinity: podAffinity("celery"),
        enableServiceLinks: false,
        securityContext: kompassiPodSecurityContext,
        containers: [
          {
            name: "master",
            image: kompassiImage,
            args: ["celery", "-A", "kompassi.celery_app:app", "worker", "-l", "DEBUG"],
            env: kompassiEnvironment,
            volumeMounts: kompassiVolumeMounts,
            securityContext: kompassiContainerSecurityContext,
          },
        ],
        volumes: kompassiVolumes,
      },
    },
  },
};

// --- NEW BACKGROUND WORKER (to replace celery at some point) ---

const workerDeployment = {
  apiVersion: "apps/v1",
  kind: "Deployment",
  metadata: { name: "worker" },
  spec: {
    selector: { matchLabels: labels("worker") },
    template: {
      metadata: { labels: labels("worker") },
      spec: {
        affinity: podAffinity("worker"),
        enableServiceLinks: false,
        securityContext: kompassiPodSecurityContext,
        containers: [
          {
            name: "main",
            image: kompassiImage,
            args: ["python", "manage.py", "tickets_v2_worker"],
            env: kompassiEnvironment,
            volumeMounts: kompassiVolumeMounts,
            securityContext: kompassiContainerSecurityContext,
          },
        ],
        volumes: kompassiVolumes,
      },
    },
  },
};

// --- NGINX (static file serving) ---

const nginxService = {
  apiVersion: "v1",
  kind: "Service",
  metadata: { name: "nginx", labels: labels("nginx") },
  spec: {
    ports: [{ port: 80, targetPort: 80 }],
    selector: labels("nginx"),
  },
};

const nginxDeployment = {
  apiVersion: "apps/v1",
  kind: "Deployment",
  metadata: { name: "nginx" },
  spec: {
    selector: { matchLabels: labels("nginx") },
    template: {
      metadata: { labels: labels("nginx") },
      spec: {
        affinity: podAffinity("nginx"),
        enableServiceLinks: false,
        containers: [
          {
            name: "master",
            image: kompassiStaticImage,
            ports: [{ containerPort: 80 }],
          },
        ],
      },
    },
  },
};

// --- INGRESS ---

const middlewaresNoTls = "default-body-100m@kubernetescrd";
const middlewaresWithTls =
  "default-https-redirect@kubernetescrd,default-body-100m@kubernetescrd";

function ingressPaths() {
  return [
    ...(env.kompassiUvicornEnabled
      ? [
          {
            pathType: "Prefix",
            path: "/api/tickets-v2",
            backend: { service: { name: "uvicorn", port: { number: 7998 } } },
          },
        ]
      : []),
    {
      pathType: "Prefix",
      path: "/static",
      backend: { service: { name: "nginx", port: { number: 80 } } },
    },
    {
      pathType: "Prefix",
      path: "/media",
      backend: { service: { name: "nginx", port: { number: 80 } } },
    },
    {
      pathType: "Prefix",
      path: "/",
      backend: { service: { name: "kompassi", port: { number: 8000 } } },
    },
  ];
}

const ingress = {
  apiVersion: "networking.k8s.io/v1",
  kind: "Ingress",
  metadata: {
    name: "kompassi",
    annotations: {
      "traefik.ingress.kubernetes.io/router.middlewares": env.ingressLetsencryptEnabled
        ? middlewaresWithTls
        : middlewaresNoTls,
      ...(env.ingressLetsencryptEnabled
        ? { "cert-manager.io/cluster-issuer": clusterIssuer }
        : {}),
    },
  },
  spec: {
    ingressClassName,
    tls: env.ingressLetsencryptEnabled
      ? [{ secretName: "ingress-letsencrypt", hosts: env.ingressPublicHostnames }]
      : [],
    rules: env.ingressPublicHostnames.map((hostname) => ({
      host: hostname,
      http: { paths: ingressPaths() },
    })),
  },
};

// kompassi-backup always has TLS (self-signed, manually managed via
// generate_backup_ingress_tls.sh), regardless of ingressLetsencryptEnabled.
const ingressBackup = {
  apiVersion: "networking.k8s.io/v1",
  kind: "Ingress",
  metadata: {
    name: "kompassi-backup",
    annotations: {
      "traefik.ingress.kubernetes.io/router.middlewares": middlewaresWithTls,
    },
  },
  spec: {
    ingressClassName,
    tls: [{ secretName: "ingress-backup", hosts: env.backupIngressPublicHostnames }],
    rules: env.backupIngressPublicHostnames.map((hostname) => ({
      host: hostname,
      http: {
        paths: [
          {
            pathType: "Prefix",
            path: "/static",
            backend: { service: { name: "nginx", port: { number: 80 } } },
          },
          {
            pathType: "Prefix",
            path: "/media",
            backend: { service: { name: "nginx", port: { number: 80 } } },
          },
          {
            pathType: "Prefix",
            path: "/",
            backend: { service: { name: "kompassi", port: { number: 8000 } } },
          },
        ],
      },
    })),
  },
};

// --- Write manifests ---

export function writeManifest(filename: string, manifest: unknown) {
  writeFileSync(filename, JSON.stringify(manifest, null, 2), { encoding: "utf-8" });
}

function removeStaleManifests(keep: Set<string>) {
  for (const filename of readdirSync(".")) {
    if (filename.endsWith(".json") && !keep.has(filename) && existsSync(filename)) {
      unlinkSync(filename);
    }
  }
}

function main() {
  mkdirSync(".", { recursive: true });
  const written = new Set<string>();

  function write(filename: string, manifest: unknown) {
    writeManifest(filename, manifest);
    written.add(filename);
  }

  if (env.redisManaged) {
    write("redis.service.json", redisService);
    write("redis.deployment.json", redisDeployment);
    if (env.redisStoragePvc) {
      write("redis.pvc.json", redisPvc);
    }
  }

  if (env.postgresManaged) {
    write("postgres.service.json", postgresService);
    write("postgres.deployment.json", postgresDeployment);
    write("postgres.pvc.json", postgresPvc);
    write("postgres.secret.json", postgresSecret);
  }

  write("kompassi.service.json", kompassiService);
  write("kompassi.deployment.json", kompassiDeployment);
  if (env.kompassiStoragePvc) {
    write("kompassi.pvc.json", kompassiPvc);
  }
  if (env.kompassiSecretManaged) {
    write("kompassi.secret.json", kompassiSecret);
  }

  if (env.kompassiUvicornEnabled) {
    write("uvicorn.service.json", uvicornService);
    write("uvicorn.deployment.json", uvicornDeployment);
  }

  if (env.kompassiCronNightlyEnabled) {
    write("cron-nightly.json", cronNightly);
  }

  write("celery.deployment.json", celeryDeployment);

  if (env.kompassiBackgroundWorkerEnabled) {
    write("worker.deployment.json", workerDeployment);
  }

  write("nginx.service.json", nginxService);
  write("nginx.deployment.json", nginxDeployment);

  write("ingress.json", ingress);
  if (env.backupIngressPublicHostnames.length > 0) {
    write("ingress-backup.json", ingressBackup);
  }

  // Remove manifests left over from a previous run with different toggles
  // (e.g. switching ENV in the same checkout).
  removeStaleManifests(written);
}

if (import.meta.url === "file://" + process.argv[1]) {
  main();
}
