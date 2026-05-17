"use server";

import { revalidatePath } from "next/cache";
import { graphql } from "@/__generated__";
import { getClient } from "@/apolloClient";

const mutation = graphql(`
  mutation UpdateInvolvementPreferences(
    $input: UpdateInvolvementPreferencesInput!
  ) {
    updateInvolvementPreferences(input: $input) {
      preferences {
        shirtsFrozenAt
      }
    }
  }
`);

export async function updateInvolvementPreferences(
  locale: string,
  eventSlug: string,
  formData: FormData,
) {
  const shirtsFrozenAtRaw = formData.get("shirtsFrozenAt");
  const shirtsFrozenAt =
    shirtsFrozenAtRaw &&
    typeof shirtsFrozenAtRaw === "string" &&
    shirtsFrozenAtRaw !== ""
      ? shirtsFrozenAtRaw
      : null;

  await getClient().mutate({
    mutation,
    variables: {
      input: {
        eventSlug,
        shirtsFrozenAt,
      },
    },
  });

  revalidatePath(`/${locale}/${eventSlug}/involvement-preferences`);
}
