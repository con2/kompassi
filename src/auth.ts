import type {
  GetServerSidePropsContext,
  NextApiRequest,
  NextApiResponse,
} from "next";
import type { NextAuthOptions as NextAuthConfig } from "next-auth";
import { getServerSession } from "next-auth";

import GitHub from "next-auth/providers/github";

// TODO
declare module "next-auth/jwt" {
  interface JWT {
    userRole?: "admin";
  }
}

export const config = {
  providers: [
    GitHub({
      clientId: process.env.GITHUB_ID,
      clientSecret: process.env.GITHUB_SECRET,
    }),
  ],
  callbacks: {
    async jwt({ token }) {
      token.userRole = "admin";
      return token;
    },
  },
} satisfies NextAuthConfig;

export function auth(
  ...args:
    | [GetServerSidePropsContext["req"], GetServerSidePropsContext["res"]]
    | [NextApiRequest, NextApiResponse]
    | []
) {
  return getServerSession(...args, config);
}

declare global {
  namespace NodeJS {
    export interface ProcessEnv {
      NEXTAUTH_SECRET: string;
      GITHUB_ID: string;
      GITHUB_SECRET: string;
    }
  }
}
