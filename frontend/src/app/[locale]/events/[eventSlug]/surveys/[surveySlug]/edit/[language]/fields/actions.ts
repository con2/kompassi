"use server";

import { revalidatePath } from "next/cache";
import { graphql } from "@/__generated__";
import { getClient } from "@/apolloClient";

const mutation = graphql(`
  mutation UpdateSurveyFieldsLanguageMutation(
    $input: UpdateSurveyLanguageInput!
  ) {
    updateSurveyLanguage(input: $input) {
      survey {
        slug
      }
    }
  }
`);

export async function updateSurveyFields(
  eventSlug: string,
  surveySlug: string,
  language: string,
  formData: FormData,
) {
  await getClient().mutate({
    mutation: mutation,
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
