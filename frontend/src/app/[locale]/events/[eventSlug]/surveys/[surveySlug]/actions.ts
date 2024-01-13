"use server";

import { redirect } from "next/navigation";

import { getClient } from "@/apolloClient";
import { gql } from "@/__generated__";

const mutation = gql(`
  mutation CreateSurveyResponse(
      $eventSlug: String!,
      $surveySlug: String!,
      $formData: GenericScalar!,
      $locale: String
  ) {
    createSurveyResponse(
      eventSlug: $eventSlug
      surveySlug: $surveySlug
      formData: $formData
      locale: $locale
    ) {
      response {
        id
      }
    }
  }
`);

export async function submit(
  locale: string,
  eventSlug: string,
  surveySlug: string,
  formData: FormData
) {
  await getClient().mutate({
    mutation,
    variables: {
      locale,
      eventSlug,
      surveySlug,
      formData: Object.fromEntries(formData),
    },
  });
  return void redirect(`/events/${eventSlug}/surveys/${surveySlug}/thanks`);
}
