"use server";

import { revalidatePath } from "next/cache";
import { graphql } from "@/__generated__";
import { getClient } from "@/apolloClient";
import { PerksOverridePayload } from "@/components/involvement/perks";

const updateInvolvementPerksMutation = graphql(`
  mutation UpdateInvolvementPerks($input: UpdateInvolvementPerksInput!) {
    updateInvolvementPerks(input: $input) {
      involvement {
        id
      }
    }
  }
`);

export async function updateInvolvementPerks(
  locale: string,
  eventSlug: string,
  personId: number,
  involvementId: string,
  payload: PerksOverridePayload,
) {
  await getClient().mutate({
    mutation: updateInvolvementPerksMutation,
    variables: {
      input: {
        eventSlug,
        involvementId,
        formData: payload,
      },
    },
  });

  revalidatePath(`/${locale}/${eventSlug}/people/${personId}`);
}
