"use server";

import { revalidatePath } from "next/cache";
import { graphql } from "@/__generated__";
import { getClient } from "@/apolloClient";

const mutation = graphql(`
  mutation UpdateQuota($input: UpdateQuotaInput!) {
    updateQuota(input: $input) {
      quota {
        id
      }
    }
  }
`);

export async function updateQuota(
  locale: string,
  eventSlug: string,
  quotaId: string,
  formData: FormData,
) {
  const input = {
    eventSlug,
    quotaId,
    formData: Object.fromEntries(formData),
  };

  await getClient().mutate({
    mutation,
    variables: { input },
  });

  revalidatePath(`/${locale}/${eventSlug}/quotas/${quotaId}`);
}
