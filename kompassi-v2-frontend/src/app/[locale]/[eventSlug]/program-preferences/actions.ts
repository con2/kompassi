"use server";

import { revalidatePath } from "next/cache";
import { graphql } from "@/__generated__";
import { getClient } from "@/apolloClient";

const mutation = graphql(`
  mutation UpdateProgramPreferences($input: UpdateProgramPreferencesInput!) {
    updateProgramPreferences(input: $input) {
      preferences {
        publicFrom
        isSchedulePublic
      }
    }
  }
`);

export async function updateProgramPreferences(
  locale: string,
  eventSlug: string,
  formData: FormData,
) {
  const publicFromRaw = formData.get("publicFrom");
  const publicFrom =
    publicFromRaw && typeof publicFromRaw === "string" && publicFromRaw !== ""
      ? publicFromRaw
      : null;

  await getClient().mutate({
    mutation,
    variables: {
      input: {
        eventSlug,
        publicFrom,
      },
    },
  });

  revalidatePath(`/${locale}/${eventSlug}/program-preferences`);
  revalidatePath(`/${locale}/${eventSlug}/program`);
}
