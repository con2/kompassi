/* eslint-disable @typescript-eslint/no-unused-vars */
import NextAuth from "next-auth";

module "next-auth" {
  interface Session {
    accessToken: string;
  }
}
