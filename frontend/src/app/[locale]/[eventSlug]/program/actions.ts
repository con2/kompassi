"use server";

import { revalidatePath } from "next/cache";
import { graphql } from "@/__generated__";
import { getClient } from "@/apolloClient";

const markScheduleItemAsFavoriteMutation = graphql(`
  mutation MarkScheduleItemAsFavorite($input: FavoriteScheduleItemInput!) {
    markScheduleItemAsFavorite(input: $input) {
      success
    }
  }
`);

export async function markScheduleItemAsFavorite(
  locale: string,
  eventSlug: string,
  scheduleItemSlug: string,
) {
  const data = await getClient().mutate({
    mutation: markScheduleItemAsFavoriteMutation,
    variables: { input: { eventSlug, scheduleItemSlug } },
  });
  revalidatePath(`/${locale}}/${eventSlug}/program`);
}

const unmarkScheduleItemAsFavoriteMutation = graphql(`
  mutation UnmarkScheduleItemAsFavorite($input: FavoriteScheduleItemInput!) {
    unmarkScheduleItemAsFavorite(input: $input) {
      success
    }
  }
`);

export async function unmarkAsFavorite(
  locale: string,
  eventSlug: string,
  scheduleItemSlug: string,
) {
  const data = await getClient().mutate({
    mutation: unmarkScheduleItemAsFavoriteMutation,
    variables: { input: { eventSlug, scheduleItemSlug } },
  });
  revalidatePath(`/${locale}}/${eventSlug}/program`);
}
