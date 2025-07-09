"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";
import { graphql } from "@/__generated__";
import { getClient } from "@/apolloClient";

const updateQuotaMutation = graphql(`
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
    mutation: updateQuotaMutation,
    variables: { input },
  });

  revalidatePath(`/${locale}/${eventSlug}/quotas/${quotaId}`);
}

const deleteQuotaMutation = graphql(`
  mutation DeleteQuota($input: DeleteQuotaInput!) {
    deleteQuota(input: $input) {
      id
    }
  }
`);

export async function deleteQuota(
  locale: string,
  eventSlug: string,
  quotaId: string,
) {
  await getClient().mutate({
    mutation: deleteQuotaMutation,
    variables: {
      input: { eventSlug, quotaId },
    },
  });

  revalidatePath(`/${locale}/${eventSlug}/quotas`);
  redirect(`/${eventSlug}/quotas`);
}
