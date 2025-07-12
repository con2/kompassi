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
const tlsSecretName = "ingress-letsencrypt";
const port = 3000;
const ingressClassName = "nginx";

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

// Startup and liveness probe
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
  NEXTAUTH_URL: publicUrl,
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
    selector: {
      matchLabels: labels(nodeServiceName),
    },
    template: {
      metadata: {
        labels: labels(nodeServiceName),
      },
      spec: {
        enableServiceLinks: false,
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
            startupProbe: probe,
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

const tls = tlsEnabled
  ? [{ hosts: [hostname], secretName: tlsSecretName }]
  : [];

const defaultIngressAnnotations = {
  "nginx.ingress.kubernetes.io/proxy-body-size": "100m",
  "nginx.org/client-max-body-size": "100m",
};
const ingressAnnotations = tlsEnabled
  ? {
      "cert-manager.io/cluster-issuer": clusterIssuer,
      "nginx.ingress.kubernetes.io/ssl-redirect": "true",
      ...defaultIngressAnnotations,
    }
  : defaultIngressAnnotations;

const ingress = {
  apiVersion: "networking.k8s.io/v1",
  kind: "Ingress",
  metadata: {
    name: stack,
    labels: labels(),
    annotations: ingressAnnotations,
  },
  spec: {
    ingressClassName,
    tls,
    rules: [
      {
        host: hostname,
        http: {
          paths: [
            {
              pathType: "Prefix",
              path: "/",
              backend: {
                service: {
                  name: nodeServiceName,
                  port: {
                    number: port,
                  },
                },
              },
            },
          ],
        },
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

function main() {
  writeManifest("deployment.json", deployment);
  writeManifest("service.json", service);
  writeManifest("ingress.json", ingress);

  if (secretManaged) {
    writeManifest("secret.json", secret);
  } else if (existsSync("secret.json")) {
    unlinkSync("secret.json");
  }
}

if (import.meta.url === "file://" + process.argv[1]) {
  main();
}
