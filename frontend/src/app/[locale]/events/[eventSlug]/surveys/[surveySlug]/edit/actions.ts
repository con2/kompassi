"use server";

import { revalidatePath } from "next/cache";
import { graphql } from "@/__generated__";
import { getClient } from "@/apolloClient";

export async function addLanguageVersion(
  eventSlug: string,
  surveySlug: string,
  formData: FormData,
) {
  // TODO stubb
  console.log("addLanguageVersion", {
    eventSlug,
    surveySlug,
    formData: Object.fromEntries(formData),
  });
}

const updateSurveyMutation = graphql(`
  mutation UpdateSurveyMutation($input: UpdateSurveyInput!) {
    updateSurvey(input: $input) {
      survey {
        slug
      }
    }
  }
`);

export async function updateSurvey(
  eventSlug: string,
  surveySlug: string,
  formData: FormData,
) {
  await getClient().mutate({
    mutation: updateSurveyMutation,
    variables: {
      input: {
        eventSlug,
        surveySlug,
        formData: Object.fromEntries(formData),
      },
    },
  });
  revalidatePath(`/events/${eventSlug}/surveys`);
}
