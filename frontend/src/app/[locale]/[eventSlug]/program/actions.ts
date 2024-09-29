"use server";

import { revalidatePath } from "next/cache";
import { graphql } from "@/__generated__";
import { FavoriteInput } from "@/__generated__/graphql";
import { getClient } from "@/apolloClient";

const markAsFavoriteMutation = graphql(`
  mutation MarkProgramAsFavorite($input: FavoriteInput!) {
    markProgramAsFavorite(input: $input) {
      success
    }
  }
`);

export async function markAsFavorite(
  locale: string,
  eventSlug: string,
  programSlug: string,
) {
  const data = await getClient().mutate({
    mutation: markAsFavoriteMutation,
    variables: { input: { eventSlug, programSlug } },
  });
  revalidatePath(`/${locale}}/${eventSlug}/program`);
}

const unmarkAsFavoriteMutation = graphql(`
  mutation UnmarkProgramAsFavorite($input: FavoriteInput!) {
    unmarkProgramAsFavorite(input: $input) {
      success
    }
  }
`);

export async function unmarkAsFavorite(
  locale: string,
  eventSlug: string,
  programSlug: string,
) {
  const data = await getClient().mutate({
    mutation: unmarkAsFavoriteMutation,
    variables: { input: { eventSlug, programSlug } },
  });
  revalidatePath(`/${locale}}/${eventSlug}/program`);
}
