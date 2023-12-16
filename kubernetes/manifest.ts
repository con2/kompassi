import { writeFileSync, unlinkSync, existsSync } from "fs";

interface Environment {
  hostname: string;
  secretManaged: boolean;
  kompassiBaseUrl: string;
  tlsEnabled: boolean;
}

type EnvironmentName = "dev" | "staging" | "production";
const environmentNames: EnvironmentName[] = ["dev", "staging", "production"];

const environmentConfigurations: Record<EnvironmentName, Environment> = {
  dev: {
    hostname: "kompassi2.localhost",
    secretManaged: true,
    kompassiBaseUrl: "https://dev.kompassi.eu",
    tlsEnabled: false,
  },
  staging: {
    hostname: "v2.dev.kompassi.eu",
    secretManaged: false,
    kompassiBaseUrl: "https://dev.kompassi.eu",
    tlsEnabled: false,
  },
  production: {
    hostname: "v2.kompassi.eu",
    secretManaged: false,
    kompassiBaseUrl: "https://kompassi.eu",
    tlsEnabled: false,
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

const { hostname, secretManaged, kompassiBaseUrl, tlsEnabled } =
  environmentConfiguration;

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
  NEXT_PUBLIC_KOMPASSI_BASE_URL: "https://kompassi.eu",
  KOMPASSI_OIDC_CLIENT_ID: secretKeyRef("KOMPASSI_OIDC_CLIENT_ID"),
  KOMPASSI_OIDC_CLIENT_SECRET: secretKeyRef("KOMPASSI_OIDC_CLIENT_SECRET"),
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
            livenessProbe: probe,
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

const ingress = {
  apiVersion: "networking.k8s.io/v1",
  kind: "Ingress",
  metadata: {
    name: stack,
    labels: labels(),
    annotations: {},
  },
  spec: {
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

if (require.main === module) {
  main();
}
