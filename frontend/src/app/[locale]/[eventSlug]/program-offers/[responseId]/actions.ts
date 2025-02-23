"use server";

import { revalidatePath } from "next/cache";

import { graphql } from "@/__generated__";
import { getClient } from "@/apolloClient";

const mutation = graphql(`
  mutation UpdateResponseDimensions($input: UpdateResponseDimensionsInput!) {
    updateResponseDimensions(input: $input) {
      response {
        id
      }
    }
  }
`);

export async function updateResponseDimensions(
  eventSlug: string,
  surveySlug: string,
  responseId: string,
  formData: FormData,
) {
  const input = {
    eventSlug,
    surveySlug,
    responseId,
    formData: Object.fromEntries(formData),
  };
  await getClient().mutate({
    mutation,
    variables: { input },
  });
  revalidatePath(`/${eventSlug}/surveys/${surveySlug}/responses`);
}
