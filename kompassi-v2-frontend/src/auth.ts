import { AuthOptions } from "next-auth";
import { getServerSession } from "next-auth/next";
import { encode as defaultEncode } from "next-auth/jwt";

import { kompassiOidc } from "@/config";

const FALLBACK_MAX_AGE = 10 * 60 * 60; // 10 hours, used only if the Kompassi token response has no expires_in

export const authOptions: AuthOptions = {
  providers: [
    {
      id: "kompassi",
      name: "Kompassi",
      type: "oauth",
      idToken: true,

      profile(profile, _tokens) {
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
  // of holding on to it for next-auth's 30-day default and hitting
  // JWT_SESSION_ERROR on every request in between.
  logger: {
    error(code, metadata) {
      if (code === "JWT_SESSION_ERROR") {
        // Expected once the JWT outlives the Kompassi access token it wraps;
        // the user will simply be prompted to log in again.
        return;
      }
      console.error(code, metadata);
    },
  },

  // persist the Kompassi access token in the session
  callbacks: {
    jwt({ token, account }) {
      if (account) {
        token.accessToken = account.access_token;
        // Kompassi's token endpoint returns expires_in, which next-auth
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

export function auth() {
  return getServerSession(authOptions);
}
