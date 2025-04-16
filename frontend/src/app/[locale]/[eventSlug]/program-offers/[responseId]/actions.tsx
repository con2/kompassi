"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";
import { graphql } from "@/__generated__";
import { getClient } from "@/apolloClient";

const mutation = graphql(`
  mutation AcceptProgramOffer($input: AcceptProgramOfferInput!) {
    acceptProgramOffer(input: $input) {
      program {
        slug
      }
    }
  }
`);

export async function acceptProgramOffer(
  locale: string,
  eventSlug: string,
  responseId: string,
  formData: FormData,
) {
  const input = {
    eventSlug,
    responseId,
    formData: Object.fromEntries(formData.entries()),
  };

  const { data, errors } = await getClient().mutate({
    mutation,
    variables: {
      input,
    },
  });

  if (errors) {
    throw new Error(errors[0].message);
  }

  const program = data?.acceptProgramOffer?.program;
  if (!program) {
    throw new Error("Program not found");
  }

  revalidatePath(`/${locale}/${eventSlug}/program-offers/${responseId}`);
  revalidatePath(`/${locale}/${eventSlug}/program-offers`);
  redirect(`/${eventSlug}/program-admin/${program.slug}`);
}
