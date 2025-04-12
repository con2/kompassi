"use server";

import { revalidatePath } from "next/cache";
import { graphql } from "@/__generated__";
import { getClient } from "@/apolloClient";

const mutation = graphql(`
  mutation UpdateProgramBasicInfo($input: UpdateProgramInput!) {
    updateProgram(input: $input) {
      program {
        slug
      }
    }
  }
`);

export async function updateProgramBasicInfo(
  locale: string,
  eventSlug: string,
  programSlug: string,
  formData: FormData,
) {
  const { data, errors } = await getClient().mutate({
    mutation,
    variables: {
      input: {
        eventSlug,
        programSlug,
        formData: Object.fromEntries(formData),
      },
    },
  });
  if (errors) {
    throw new Error(errors[0].message);
  }

  revalidatePath(`/${locale}/${eventSlug}/program-admin/${programSlug}`);
  revalidatePath(`/${locale}/${eventSlug}/program-admin`);
}
