"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";
import { graphql } from "@/__generated__";
import { getClient } from "@/apolloClient";

const deleteProgramOffersMutation = graphql(`
  mutation DeleteProgramOffers($input: DeleteProgramOffersInput!) {
    deleteProgramOffers(input: $input) {
      countDeleted
    }
  }
`);

export async function deleteProgramOffers(
  locale: string,
  eventSlug: string,
  programOfferIds: string[],
  searchParams: Record<string, string> | null = null,
): Promise<void> {
  await getClient().mutate({
    mutation: deleteProgramOffersMutation,
    variables: {
      input: {
        eventSlug,
        programOfferIds,
      },
    },
  });

  const queryString =
    searchParams && Object.entries(searchParams).length > 0
      ? "?" + new URLSearchParams(searchParams).toString()
      : "";

  revalidatePath(`/${locale}/${eventSlug}/program-offers`);
  redirect(`/${locale}/${eventSlug}/program-offers${queryString}`);
}
