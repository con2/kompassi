import { writeFileSync, unlinkSync, existsSync } from "fs";

interface Environment {
  hostname: string;
  secretManaged: boolean;
  kompassiBaseUrl: string;
  tlsEnabled: boolean;
  ticketsApiUrl: string;
  livenessProbeEnabled: boolean;
}

type EnvironmentName = "dev" | "staging" | "production";
const environmentNames: EnvironmentName[] = ["dev", "staging", "production"];

const environmentConfigurations: Record<EnvironmentName, Environment> = {
  dev: {
    hostname: "kompassi2.localhost",
    secretManaged: true,
    kompassiBaseUrl: "https://dev.kompassi.eu",
    tlsEnabled: false,
    // as an optimization, access the tickets API directly without going through the ingress
    ticketsApiUrl: "http://uvicorn.default.svc.cluster.local:7998",
    livenessProbeEnabled: true,
  },
  staging: {
    hostname: "v2.dev.kompassi.eu",
    secretManaged: false,
    kompassiBaseUrl: "https://dev.kompassi.eu",
    tlsEnabled: true,
    ticketsApiUrl: "http://uvicorn.kompassi-staging.svc.cluster.local:7998",
    livenessProbeEnabled: true,
  },
  production: {
    hostname: "v2.kompassi.eu",
    secretManaged: false,
    kompassiBaseUrl: "https://kompassi.eu",
    tlsEnabled: true,
    ticketsApiUrl: "http://uvicorn.kompassi-production.svc.cluster.local:7998",
    livenessProbeEnabled: false, // TODO re-enable after Hunger Games
  },
};

function getEnvironmentName(): EnvironmentName {
  const environmentName = process.env.ENV;
  if (!environmentNames.includes(environmentName as EnvironmentName)) {
    return "dev";
  }
  return environmentName as EnvironmentName;
}

const environmentConfiguration =
  environmentConfigurations[getEnvironmentName()];

export const stack = "kompassi2";
const image = "kompassi2";
const nodeServiceName = "node";
const clusterIssuer = "letsencrypt-prod";
// Same Secret name the Ingress used, so the existing certificate is adopted.
const tlsSecretName = "ingress-letsencrypt";
const port = 3000;
const gatewayClassName = "traefik";

const {
  hostname,
  secretManaged,
  kompassiBaseUrl,
  tlsEnabled,
  ticketsApiUrl,
  livenessProbeEnabled,
} = environmentConfiguration;

const ingressProtocol = tlsEnabled ? "https" : "http";
const publicUrl = `${ingressProtocol}://${hostname}`;

// Liveness probe
const probe = {
  httpGet: {
    path: "/healthz",
    port,
    httpHeaders: [
      {
        name: "host",
        value: hostname,
      },
    ],
  },
};

const startupProbe = {
  ...probe,
  periodSeconds: 2,
  failureThreshold: 60,
};

export function labels(component?: string) {
  return {
    stack,
    component,
  };
}

function secretKeyRef(key: string) {
  return {
    secretKeyRef: {
      name: stack,
      key,
    },
  };
}

const env = Object.entries({
  PORT: port,
  NEXTAUTH_SECRET: secretKeyRef("NEXTAUTH_SECRET"),
  AUTH_URL: publicUrl,
  NEXT_PUBLIC_KOMPASSI_BASE_URL: kompassiBaseUrl,
  KOMPASSI_OIDC_CLIENT_ID: secretKeyRef("KOMPASSI_OIDC_CLIENT_ID"),
  KOMPASSI_OIDC_CLIENT_SECRET: secretKeyRef("KOMPASSI_OIDC_CLIENT_SECRET"),
  KOMPASSI_TICKETS_V2_API_URL: ticketsApiUrl,
  KOMPASSI_TICKETS_V2_API_KEY: secretKeyRef("KOMPASSI_TICKETS_V2_API_KEY"),
}).map(([key, value]) => {
  if (value instanceof Object) {
    return {
      name: key,
      valueFrom: value,
    };
  } else {
    return {
      name: key,
      value: String(value),
    };
  }
});

const volumes = [
  {
    name: "kompassi2-temp",
    emptyDir: {},
  },
];

const volumeMounts = [
  {
    name: "kompassi2-temp",
    mountPath: "/usr/src/app/.next/cache",
  },
];

const deployment = {
  apiVersion: "apps/v1",
  kind: "Deployment",
  metadata: {
    name: nodeServiceName,
    labels: labels(nodeServiceName),
  },
  spec: {
    // Roll one pod at a time, never below the current count. Traefik keeps a
    // terminating pod in its backend list for a few seconds after Kubernetes
    // starts removing its endpoint; the preStop sleep keeps the pod serving
    // through that window instead of returning 502s on every deploy.
    strategy: {
      type: "RollingUpdate",
      rollingUpdate: { maxSurge: 1, maxUnavailable: 0 },
    },
    selector: {
      matchLabels: labels(nodeServiceName),
    },
    template: {
      metadata: {
        labels: labels(nodeServiceName),
      },
      spec: {
        enableServiceLinks: false,
        terminationGracePeriodSeconds: 45,
        securityContext: {
          runAsUser: 1000,
          runAsGroup: 1000,
          fsGroup: 1000,
        },
        volumes,
        initContainers: [],
        containers: [
          {
            name: nodeServiceName,
            image,
            env,
            ports: [{ containerPort: port }],
            securityContext: {
              readOnlyRootFilesystem: false,
              allowPrivilegeEscalation: false,
            },
            lifecycle: { preStop: { sleep: { seconds: 10 } } },
            startupProbe,
            livenessProbe: livenessProbeEnabled ? probe : undefined,
            volumeMounts,
          },
        ],
      },
    },
  },
};

const service = {
  apiVersion: "v1",
  kind: "Service",
  metadata: {
    name: nodeServiceName,
    labels: labels(nodeServiceName),
  },
  spec: {
    ports: [
      {
        port,
        targetPort: port,
      },
    ],
    selector: labels(nodeServiceName),
  },
};

// One Gateway per namespace. With TLS, cert-manager issues the certificate for the
// https listener from the cluster-issuer annotation into tlsSecretName. Without TLS
// (local dev) there is only the http listener and no redirect.
const gateway = {
  apiVersion: "gateway.networking.k8s.io/v1",
  kind: "Gateway",
  metadata: {
    name: stack,
    labels: labels(),
    ...(tlsEnabled
      ? { annotations: { "cert-manager.io/cluster-issuer": clusterIssuer } }
      : {}),
  },
  spec: {
    gatewayClassName,
    listeners: [
      {
        name: "http",
        protocol: "HTTP",
        port: 80,
        hostname,
        allowedRoutes: { namespaces: { from: "Same" } },
      },
      ...(tlsEnabled
        ? [
            {
              name: "https",
              protocol: "HTTPS",
              port: 443,
              hostname,
              tls: {
                mode: "Terminate",
                certificateRefs: [{ kind: "Secret", name: tlsSecretName }],
              },
              allowedRoutes: { namespaces: { from: "Same" } },
            },
          ]
        : []),
    ],
  },
};

// An HTTPRoute can only reference Middlewares in its own namespace, so the ones
// shared in `default` for Ingress apps are duplicated here.
const bodyLimitMiddleware = {
  apiVersion: "traefik.io/v1alpha1",
  kind: "Middleware",
  metadata: { name: "body-100m", labels: labels() },
  spec: { buffering: { maxRequestBodyBytes: 100_000_000 } },
};

// Retries only when the backend never answered (connection refused/reset) and
// only for idempotent methods, covering the moment a pod stops accepting
// connections during a rollout.
const retryMiddleware = {
  apiVersion: "traefik.io/v1alpha1",
  kind: "Middleware",
  metadata: { name: "retry", labels: labels() },
  spec: { retry: { attempts: 3, initialInterval: "100ms" } },
};

function middlewareFilter(name: string) {
  return {
    type: "ExtensionRef",
    extensionRef: { group: "traefik.io", kind: "Middleware", name },
  };
}

// Redirects are done per app instead of at the Traefik entrypoint so cert-manager's
// plain-HTTP solver Ingress keeps working. Attached to the http listener by name:
// without sectionName it would also attach to the https listener and loop.
const httpsRedirectRoute = {
  apiVersion: "gateway.networking.k8s.io/v1",
  kind: "HTTPRoute",
  metadata: { name: "redirect-https", labels: labels() },
  spec: {
    parentRefs: [{ name: stack, sectionName: "http" }],
    hostnames: [hostname],
    rules: [
      {
        filters: [
          {
            type: "RequestRedirect",
            requestRedirect: { scheme: "https", statusCode: 301 },
          },
        ],
      },
    ],
  },
};

const httpRoute = {
  apiVersion: "gateway.networking.k8s.io/v1",
  kind: "HTTPRoute",
  metadata: { name: stack, labels: labels() },
  spec: {
    parentRefs: [{ name: stack, sectionName: tlsEnabled ? "https" : "http" }],
    hostnames: [hostname],
    rules: [
      {
        matches: [{ path: { type: "PathPrefix", value: "/" } }],
        filters: [
          middlewareFilter(bodyLimitMiddleware.metadata.name),
          middlewareFilter(retryMiddleware.metadata.name),
        ],
        backendRefs: [{ name: nodeServiceName, port }],
      },
    ],
  },
};

export function b64(str: string) {
  return Buffer.from(str).toString("base64");
}

// only written if secretManaged is true
const secret = {
  apiVersion: "v1",
  kind: "Secret",
  type: "Opaque",
  metadata: {
    name: stack,
    labels: labels(),
  },
  data: {
    KOMPASSI_OIDC_CLIENT_SECRET: b64("kompassi_insecure_test_client_secret"),
    KOMPASSI_OIDC_CLIENT_ID: b64("kompassi_insecure_test_client_id"),
    NEXTAUTH_SECRET: b64("eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee"),
    KOMPASSI_TICKETS_V2_API_KEY: b64("kompassi_insecure_test_api_key"),
  },
};

export function writeManifest(filename: string, manifest: unknown) {
  writeFileSync(filename, JSON.stringify(manifest, null, 2), {
    encoding: "utf-8",
  });
}

// Removes a stale file from an earlier run with a different ENV, since
// skaffold deploys every JSON file in this directory.
function writeManifestIf(
  condition: boolean,
  filename: string,
  manifest: unknown,
) {
  if (condition) {
    writeManifest(filename, manifest);
  } else if (existsSync(filename)) {
    unlinkSync(filename);
  }
}

function main() {
  writeManifest("deployment.json", deployment);
  writeManifest("service.json", service);
  writeManifest("gateway.json", gateway);
  writeManifest("middleware-body-100m.json", bodyLimitMiddleware);
  writeManifest("middleware-retry.json", retryMiddleware);
  writeManifest("httproute-kompassi2.json", httpRoute);

  writeManifestIf(
    tlsEnabled,
    "httproute-redirect-https.json",
    httpsRedirectRoute,
  );
  writeManifestIf(secretManaged, "secret.json", secret);
}

if (import.meta.url === "file://" + process.argv[1]) {
  main();
}
