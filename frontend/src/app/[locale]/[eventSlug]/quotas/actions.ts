"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";
import { graphql } from "@/__generated__";
import { getClient } from "@/apolloClient";

const mutation = graphql(`
  mutation CreateQuota($input: CreateQuotaInput!) {
    createQuota(input: $input) {
      quota {
        id
      }
    }
  }
`);

export async function createQuota(
  locale: string,
  eventSlug: string,
  formData: FormData,
) {
  const result = await getClient().mutate({
    mutation,
    variables: {
      input: {
        eventSlug,
        formData: Object.fromEntries(formData),
      },
    },
  });

  revalidatePath(`/${locale}/${eventSlug}/quotas`);

  const newQuotaId = result.data?.createQuota?.quota?.id;
  redirect(`/${eventSlug}/quotas/${newQuotaId ?? ""}`);
}
