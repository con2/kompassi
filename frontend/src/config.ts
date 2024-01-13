export const kompassiBaseUrl =
  process.env.NEXT_PUBLIC_KOMPASSI_BASE_URL || "https://dev.kompassi.eu";

export const kompassiOidc = {
  wellKnown:
    process.env.KOMPASSI_OIDC_WELL_KNOWN ||
    `${kompassiBaseUrl}/oidc/.well-known/openid-configuration/`,
  clientId:
    process.env.KOMPASSI_OIDC_CLIENT_ID || "kompassi_insecure_test_client_id",
  clientSecret:
    process.env.KOMPASSI_OIDC_CLIENT_SECRET ||
    "kompassi_insecure_test_client_secret",
};

export const publicUrl = process.env.NEXTAUTH_URL || "http://localhost:3000";
