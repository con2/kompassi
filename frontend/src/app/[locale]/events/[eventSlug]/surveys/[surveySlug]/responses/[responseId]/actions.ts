"use server";

import { revalidatePath } from "next/cache";

import { gql } from "@/__generated__";
import { getClient } from "@/apolloClient";

const mutation = gql(`
  mutation UpdateResponseDimensions(
      $eventSlug: String!,
      $surveySlug: String!,
      $responseId: String!,
      $formData: GenericScalar!,
  ) {
    updateResponseDimensions(
      eventSlug: $eventSlug
      surveySlug: $surveySlug
      responseId: $responseId
      formData: $formData
    ) {
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
  await getClient().mutate({
    mutation,
    variables: {
      eventSlug,
      surveySlug,
      responseId,
      formData: Object.fromEntries(formData),
    },
  });
  revalidatePath(`/events/${eventSlug}/surveys/${surveySlug}/responses`);
}
