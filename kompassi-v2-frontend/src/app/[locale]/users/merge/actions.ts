"use server";

import { redirect } from "next/navigation";

import { graphql } from "@/__generated__";
import { getClient, graphqlErrorCode } from "@/apolloClient";

const mergePeopleMutation = graphql(`
  mutation MergePeople($input: MergePeopleInput!) {
    mergePeople(input: $input) {
      person {
        id
      }
    }
  }
`);

const MERGE_CONFLICT = "MERGE_CONFLICT";

export async function mergePeople(
  intoPersonId: number,
  mergePersonIds: number[],
) {
  const personIds = [intoPersonId, ...mergePersonIds].join(",");

  try {
    await getClient().mutate({
      mutation: mergePeopleMutation,
      variables: { input: { intoPersonId, mergePersonIds } },
    });
  } catch (error) {
    if (graphqlErrorCode(error) === MERGE_CONFLICT) {
      return void redirect(
        `/users/merge?ids=${personIds}&into=${intoPersonId}&error=mergeConflict`,
      );
    }
    throw error;
  }

  redirect(`/users/${intoPersonId}?success=merged`);
}
