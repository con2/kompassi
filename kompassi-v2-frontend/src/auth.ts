import { AuthOptions } from "next-auth";
import { getServerSession } from "next-auth/next";

import { kompassiOidc } from "@/config";

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

  // TODO make this expire at the same time as the Kompassi access token
  // currently we just assume this is the validity period of the Kompassi access token
  session: {
    maxAge: 10 * 60 * 60, // 10 hours
  },
  jwt: {
    maxAge: 10 * 60 * 60, // 10 hours
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
