import { Temporal } from "@js-temporal/polyfill";

export const kompassiBaseUrl =
  process.env.NEXT_PUBLIC_KOMPASSI_BASE_URL || "https://dev.kompassi.eu";

export const ticketsApiKey = process.env.KOMPASSI_TICKETS_V2_API_KEY || "";

// Use this to form URLs that need to be accessed by the browser.
export const ticketsBaseUrl =
  process.env.NEXT_PUBLIC_TICKETS_BASE_URL || kompassiBaseUrl;

// Use this to form URLs that need to be accessed by the server.
export const ticketsApiUrl =
  process.env.KOMPASSI_TICKETS_V2_API_URL || `${ticketsBaseUrl}/api/tickets-v2`;

export const kompassiOidc = {
  wellKnown: `${kompassiBaseUrl}/oidc/.well-known/openid-configuration/`,
  clientId:
    process.env.KOMPASSI_OIDC_CLIENT_ID || "kompassi_insecure_test_client_id",
  clientSecret:
    process.env.KOMPASSI_OIDC_CLIENT_SECRET ||
    "kompassi_insecure_test_client_secret",
};

export const publicUrl = process.env.NEXTAUTH_URL || "http://localhost:3000";

export const timezone = process.env.KOMPASSI_TIMEZONE || "Europe/Helsinki";
