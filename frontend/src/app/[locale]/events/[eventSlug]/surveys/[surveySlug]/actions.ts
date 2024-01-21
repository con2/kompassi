"use server";

import { redirect } from "next/navigation";

import { gql } from "@/__generated__";
import { getClient } from "@/apolloClient";

const mutation = gql(`
  mutation CreateSurveyResponse($input: CreateSurveyResponseInput!) {
    createSurveyResponse(input: $input) {
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
  formData: FormData,
) {
  const input = {
    locale,
    eventSlug,
    surveySlug,
    formData: Object.fromEntries(formData),
  };
  await getClient().mutate({
    mutation,
    variables: { input },
  });
  return void redirect(`/events/${eventSlug}/surveys/${surveySlug}/thanks`);
}
