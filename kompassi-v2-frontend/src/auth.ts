import NextAuth, { type NextAuthConfig } from "next-auth";
import { encode as defaultEncode } from "next-auth/jwt";

import { authSecret, kompassiOidc } from "@/config";

const FALLBACK_MAX_AGE = 10 * 60 * 60; // 10 hours, used only if the Kompassi token response has no expires_in

const config: NextAuthConfig = {
  secret: authSecret,
  // The app is only ever reached through the cluster ingress, which sets the Host header itself.
  trustHost: true,
  providers: [
    {
      id: "kompassi",
      name: "Kompassi",
      type: "oidc",
      // PKCE binds the code to this login, nonce binds the ID token to it; PKCE alone is the default.
      checks: ["pkce", "state", "nonce"],

      profile(profile) {
        return {
          image: null,
          id: profile.sub,
          name: profile.name,
          email: profile.email,
        };
      },
      ...kompassiOidc,
    },
  ],

  session: {
    maxAge: FALLBACK_MAX_AGE,
  },
  jwt: {
    maxAge: FALLBACK_MAX_AGE,

    // The default encode() always sets exp = now + maxAge, ignoring any exp
    // already on the token. We want the session JWT to expire together with
    // the Kompassi access token it carries (set as token.exp in the jwt
    // callback below), so re-derive maxAge from that when present.
    encode(params) {
      const exp = params.token?.exp;
      const maxAge =
        typeof exp === "number"
          ? exp - Math.floor(Date.now() / 1000)
          : params.maxAge;
      return defaultEncode({ ...params, maxAge });
    },
  },

  // session.maxAge above also governs the session cookie's Max-Age, so the
  // browser drops the cookie once the JWT inside it would be stale, instead
  // of holding on to it for Auth.js's 30-day default and hitting
  // JWTSessionError on every request in between.
  logger: {
    error(error) {
      if (error.name === "JWTSessionError") {
        // Expected once the JWT outlives the Kompassi access token it wraps;
        // the user will simply be prompted to log in again.
        return;
      }
      console.error(error);
    },
  },

  // persist the Kompassi access token in the session
  callbacks: {
    jwt({ token, account }) {
      if (account) {
        token.accessToken = account.access_token;
        // Kompassi's token endpoint returns expires_in, which Auth.js
        // normalizes into expires_at; mirror it so the session JWT (see
        // jwt.encode above) expires together with the access token instead
        // of the FALLBACK_MAX_AGE guess.
        if (typeof account.expires_at === "number") {
          token.exp = account.expires_at;
        }
      }
      return token;
    },
    session({ session, token }) {
      session.accessToken = token.accessToken as string;
      return session;
    },
  },
};

export const { handlers, auth } = NextAuth(config);
