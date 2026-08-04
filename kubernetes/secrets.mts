// usage: node --experimental-strip-types secrets.mts
// run from the directory where you want the secrets generated
// generates minimal secret json to apply manually in kubernetes
import { writeFileSync } from "fs";

function b64(str: string) {
  return Buffer.from(str).toString("base64");
}

const stack = "kompassi";
function labels(component?: string) {
  return { stack, component };
}

const env = {
  postgresHostname: "postgres",
  postgresUsername: "kompassi",
  postgresDatabase: "kompassi",
  postgresPassword: "secret",
  kompassiSecretKey: "not a very secret key",
  minioAccessKeyId: "minio-access-key-kompassi",
  minioSecretAccessKey: "minio-secret-access-key-kompassi",
};

const postgresSecret = {
  apiVersion: "v1",
  kind: "Secret",
  metadata: {
    name: "postgres",
    labels: labels("postgres"),
  },
  type: "Opaque",
  data: {
    username: b64(env.postgresUsername),
    hostname: b64(env.postgresHostname),
    database: b64(env.postgresDatabase),
    password: env.postgresPassword ? b64(env.postgresPassword) : undefined,
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

export function writeSecret(filename: string, manifest: unknown) {
  writeFileSync(filename, JSON.stringify(manifest, null, 2), {
    encoding: "utf-8",
  });
}

function main() {
  writeSecret("kompassi.secret.json", kompassiSecret);
  writeSecret("postgres.secret.json", postgresSecret);
}

if (import.meta.url === "file://" + process.argv[1]) {
  main();
}
