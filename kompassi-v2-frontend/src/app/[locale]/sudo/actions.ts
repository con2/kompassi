"use server";

import { redirect } from "next/navigation";
import { graphql } from "@/__generated__";
import { getClient } from "@/apolloClient";
import isSiteRelativePath from "@/helpers/isSiteRelativePath";

const sudoCbacMutation = graphql(`
  mutation SudoCbac($input: SudoCbacInput!) {
    sudoCbac(input: $input) {
      validUntil
    }
  }
`);

export async function sudoCbac(next: string, claims: Record<string, string>) {
  await getClient().mutate({
    mutation: sudoCbacMutation,
    variables: { input: { claims } },
  });

  redirect(isSiteRelativePath(next) ? next : "/");
}
