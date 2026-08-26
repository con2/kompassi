// Generate Kubernetes manifests based on environment variables.
// See https://github.com/japsu/depleten for philosophy, and
// kompassi-v2-frontend/kubernetes/manifest.ts for a smaller sibling example.
// Usage: ENV=staging node --experimental-strip-types manifest.mts
// (intended to be run with this file's own directory as the cwd)

import { writeFileSync } from "fs";

export const stack = "kompassi";
const kompassiImage = "kompassi"; // image name/tag managed by skaffold
const kompassiStaticImage = "kompassi-static";
const ingressClassName = "traefik";
const clusterIssuer = "letsencrypt-prod";

interface Environment {
  ingressPublicHostnames: string[];
  installationSlug: string;
  installationName: string;
  baseUrl: string;
  v2BaseUrl: string;
  ticketsV2ApiUrl: string;
  allowedLoginRedirects: string[];
  admins: string[];
  workers: number;
  timeoutSeconds: number;
  cronNightlySuspended: boolean;
  cronFrequentSuspended: boolean;
  readinessProbeEnabled: boolean;
  livenessProbeEnabled: boolean;
  postgresSsl: boolean;
  redisHostname: string;
  redisBrokerDatabase: number;
  redisCacheDatabase: number;
  minioBucketName: string;
  minioEndpointUrl: string;
  smtpServer: string;
  smtpDefaultFromEmail: string;
}

type EnvironmentName = "staging" | "production";
const environmentNames: EnvironmentName[] = ["staging", "production"];

const base = {
  workers: 4,
  timeoutSeconds: 120,
  cronNightlySuspended: false,
  cronFrequentSuspended: false,
  readinessProbeEnabled: true,
  livenessProbeEnabled: true,
  admins: ["Luka Pajukanta <santtu@pajukanta.fi>"],
  postgresSsl: true,
  redisHostname: "redis-ha-haproxy.redis-ha.svc.cluster.local",
  minioEndpointUrl: "https://minio.con2.fi",
  smtpServer: "sr1.pahaip.fi",
  smtpDefaultFromEmail: "suunnistajat@kompassi.eu",
};

const environments: Record<EnvironmentName, Environment> = {
  staging: {
    ...base,
    ingressPublicHostnames: ["dev.kompassi.eu"],
    redisBrokerDatabase: 7,
    redisCacheDatabase: 7,
    installationName: "Kompassi (DEV)",
    installationSlug: "turskadev",
    baseUrl: "https://dev.kompassi.eu",
    v2BaseUrl: "https://v2.dev.kompassi.eu",
    ticketsV2ApiUrl: "http://uvicorn.kompassi-staging.svc.cluster.local:7998",
    allowedLoginRedirects: [
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
    minioBucketName: "kompassidev",
  },
  production: {
    ...base,
    ingressPublicHostnames: ["kompassi.eu", "conit.fi"],
    redisBrokerDatabase: 9,
    redisCacheDatabase: 9,
    installationName: "Kompassi",
    installationSlug: "turska",
    baseUrl: "https://kompassi.eu",
    v2BaseUrl: "https://v2.kompassi.eu",
    ticketsV2ApiUrl:
      "http://uvicorn.kompassi-production.svc.cluster.local:7998",
    allowedLoginRedirects: [
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
    workers: 12,
    minioBucketName: "kompassi",
  },
};

function getEnvironmentName(): EnvironmentName {
  const environmentName = process.env.ENV;
  if (!environmentNames.includes(environmentName as EnvironmentName)) {
    throw new Error("set ENV=staging|production");
  }
  return environmentName as EnvironmentName;
}

const environmentName = getEnvironmentName();
const env: Environment = environments[environmentName];

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

export function labels(component?: string) {
  return { stack, component };
}

function secretKeyRef(name: string, key: string) {
  return { secretKeyRef: { name, key } };
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
  ALLOWED_HOSTS: env.ingressPublicHostnames.join(" "),
  EMAIL_HOST: env.smtpServer,
  DEFAULT_FROM_EMAIL: env.smtpDefaultFromEmail,
  ADMINS: env.admins.join(","),
  KOMPASSI_INSTALLATION_NAME: env.installationName,
  KOMPASSI_INSTALLATION_SLUG: env.installationSlug,
  KOMPASSI_BASE_URL: env.baseUrl,
  KOMPASSI_V2_BASE_URL: env.v2BaseUrl,
  KOMPASSI_TICKETS_V2_API_URL: env.ticketsV2ApiUrl,
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
  KOMPASSI_CSP_ALLOWED_LOGIN_REDIRECTS: env.allowedLoginRedirects.join(" "),
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
  value instanceof Object
    ? { name, valueFrom: value }
    : { name, value: String(value) },
);

const kompassiVolumeMounts = [
  { mountPath: "/usr/src/app/media", name: "kompassi-media" },
  { mountPath: "/tmp", name: "kompassi-temp" },
  { mountPath: "/mnt/secrets/kompassi", name: "kompassi-secret" },
];

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
  { name: "kompassi-media", emptyDir: {} }, // media goes to minio
];

function probe(path: string, port: number) {
  return {
    httpGet: {
      path,
      port,
      httpHeaders: [{ name: "Host", value: primaryHostname }],
    },
  };
}

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
        initContainers: [
          {
            name: "setup",
            image: kompassiImage,
            args: ["python", "manage.py", "setup"],
            env: kompassiEnvironment,
            securityContext: kompassiContainerSecurityContext,
          },
        ],
        containers: [
          {
            name: "master",
            image: kompassiImage,
            ports: [{ containerPort: 8000 }],
            env: kompassiEnvironment,
            securityContext: kompassiContainerSecurityContext,
            args: [
              "gunicorn",
              `--workers=${env.workers}`,
              "--bind=0.0.0.0:8000",
              "--capture-output",
              `--timeout=${env.timeoutSeconds}`,
              "kompassi.wsgi",
            ],
            startupProbe: probe("/api/v1/status", 8000),
            readinessProbe: env.readinessProbeEnabled
              ? { ...probe("/api/v1/status", 8000), periodSeconds: 30 }
              : undefined,
            livenessProbe: env.livenessProbeEnabled
              ? {
                  ...probe("/api/v1/status", 8000),
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
              `--workers=${env.workers}`,
              "kompassi.tickets_v2.optimized_server.app:app",
            ],
            startupProbe: probe("/api/tickets-v2/status", 7998),
            readinessProbe: {
              ...probe("/api/tickets-v2/status", 7998),
              periodSeconds: 30,
            },
            livenessProbe: {
              ...probe("/api/tickets-v2/status", 7998),
              initialDelaySeconds: 15,
              periodSeconds: 30,
            },
          },
        ],
      },
    },
  },
};

const cronNightly = {
  apiVersion: "batch/v1",
  kind: "CronJob",
  metadata: { name: "cron-nightly" },
  spec: {
    schedule: "7 0 * * *",
    successfulJobsHistoryLimit: 1,
    failedJobsHistoryLimit: 3,
    concurrencyPolicy: "Forbid",
    suspend: env.cronNightlySuspended,
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

const cronFrequent = {
  apiVersion: "batch/v1",
  kind: "CronJob",
  metadata: { name: "cron-frequent" },
  spec: {
    schedule: "*/5 * * * *",
    successfulJobsHistoryLimit: 1,
    failedJobsHistoryLimit: 3,
    concurrencyPolicy: "Forbid",
    suspend: env.cronFrequentSuspended,
    jobTemplate: {
      spec: {
        template: {
          metadata: { labels: labels("cron-frequent") },
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
                args: ["python", "manage.py", "cron_frequent"],
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
            args: [
              "celery",
              "-A",
              "kompassi.celery_app:app",
              "worker",
              "-l",
              "DEBUG",
            ],
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

const ingress = {
  apiVersion: "networking.k8s.io/v1",
  kind: "Ingress",
  metadata: {
    name: "kompassi",
    annotations: {
      "traefik.ingress.kubernetes.io/router.middlewares":
        "default-https-redirect@kubernetescrd,default-body-100m@kubernetescrd",
      "cert-manager.io/cluster-issuer": clusterIssuer,
    },
  },
  spec: {
    ingressClassName,
    tls: [
      {
        secretName: "ingress-letsencrypt",
        hosts: env.ingressPublicHostnames,
      },
    ],
    rules: env.ingressPublicHostnames.map((hostname) => ({
      host: hostname,
      http: {
        paths: [
          {
            pathType: "Prefix",
            path: "/api/tickets-v2",
            backend: { service: { name: "uvicorn", port: { number: 7998 } } },
          },
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

export function writeManifest(filename: string, manifest: unknown) {
  writeFileSync(filename, JSON.stringify(manifest, null, 2), {
    encoding: "utf-8",
  });
}

function main() {
  writeManifest("kompassi.service.json", kompassiService);
  writeManifest("kompassi.deployment.json", kompassiDeployment);

  writeManifest("uvicorn.service.json", uvicornService);
  writeManifest("uvicorn.deployment.json", uvicornDeployment);

  writeManifest("cron-nightly.json", cronNightly);
  writeManifest("cron-frequent.json", cronFrequent);

  writeManifest("celery.deployment.json", celeryDeployment);

  writeManifest("worker.deployment.json", workerDeployment);

  writeManifest("nginx.service.json", nginxService);
  writeManifest("nginx.deployment.json", nginxDeployment);

  writeManifest("ingress.json", ingress);
}

if (import.meta.url === "file://" + process.argv[1]) {
  main();
}
