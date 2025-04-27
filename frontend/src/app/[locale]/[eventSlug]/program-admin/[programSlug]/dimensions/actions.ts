"use server";

import { revalidatePath } from "next/cache";

import { graphql } from "@/__generated__";
import { getClient } from "@/apolloClient";

const mutation = graphql(`
  mutation UpdateProgramDimensions($input: UpdateProgramDimensionsInput!) {
    updateProgramDimensions(input: $input) {
      program {
        slug
      }
    }
  }
`);

export async function updateProgramDimensions(
  eventSlug: string,
  programSlug: string,
  formData: FormData,
) {
  const input = {
    eventSlug,
    programSlug,
    formData: Object.fromEntries(formData),
  };
  await getClient().mutate({
    mutation,
    variables: { input },
  });
  revalidatePath(`/${eventSlug}/program-admin/${programSlug}/dimensions`);
}
