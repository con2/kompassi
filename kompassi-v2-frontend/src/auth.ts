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

  jwt: {
    // TODO make this expire at the same time as the Kompassi access token
    // currently we just assume this is the validity period of the Kompassi access token
    maxAge: 10 * 60 * 60, // 10 hours
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
