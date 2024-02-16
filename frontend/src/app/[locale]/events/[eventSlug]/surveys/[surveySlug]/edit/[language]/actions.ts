"use server";

import { revalidatePath } from "next/cache";
import { graphql } from "@/__generated__";
import { getClient } from "@/apolloClient";

const updateSurveyLanguageMutation = graphql(`
  mutation UpdateSurveyLanguageMutation($input: UpdateSurveyLanguageInput!) {
    updateSurveyLanguage(input: $input) {
      survey {
        slug
      }
    }
  }
`);

export async function updateSurveyLanguage(
  eventSlug: string,
  surveySlug: string,
  language: string,
  formData: FormData,
) {
  await getClient().mutate({
    mutation: updateSurveyLanguageMutation,
    variables: {
      input: {
        eventSlug,
        surveySlug,
        language,
        formData: Object.fromEntries(formData),
      },
    },
  });
  revalidatePath(`/events/${eventSlug}/surveys`);
}
