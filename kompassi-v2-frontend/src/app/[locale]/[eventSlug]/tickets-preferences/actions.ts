"use server";

import { revalidatePath } from "next/cache";
import { graphql } from "@/__generated__";
import { getClient } from "@/apolloClient";

const mutation = graphql(`
  mutation UpdateTicketsPreferences($input: UpdateTicketsPreferencesInput!) {
    updateTicketsPreferences(input: $input) {
      preferences {
        contactEmail
        termsAndConditionsUrlEn
        termsAndConditionsUrlFi
        termsAndConditionsUrlSv
        cancellationPeriodDays
      }
    }
  }
`);

export async function updateTicketsPreferences(
  locale: string,
  eventSlug: string,
  formData: FormData,
) {
  const cancellationPeriodDays =
    parseInt("" + formData.get("cancellationPeriodDays"), 10) || 0;

  await getClient().mutate({
    mutation,
    variables: {
      input: {
        eventSlug,
        contactEmail: "" + (formData.get("contactEmail") ?? ""),
        termsAndConditionsUrlEn:
          "" + (formData.get("termsAndConditionsUrlEn") ?? ""),
        termsAndConditionsUrlFi:
          "" + (formData.get("termsAndConditionsUrlFi") ?? ""),
        termsAndConditionsUrlSv:
          "" + (formData.get("termsAndConditionsUrlSv") ?? ""),
        cancellationPeriodDays,
      },
    },
  });

  revalidatePath(`/${locale}/${eventSlug}/tickets-preferences`);
}
