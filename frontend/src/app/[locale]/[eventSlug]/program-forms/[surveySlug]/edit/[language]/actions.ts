"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";
import { graphql } from "@/__generated__";
import { getClient } from "@/apolloClient";

const updateFormMutation = graphql(`
  mutation UpdateFormMutation($input: UpdateFormInput!) {
    updateForm(input: $input) {
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
    mutation: updateFormMutation,
    variables: {
      input: {
        eventSlug,
        surveySlug,
        language,
        formData: Object.fromEntries(formData),
      },
    },
  });
  revalidatePath(`/${eventSlug}/surveys`);
}

const deleteSurveyLanguageMutation = graphql(`
  mutation DeleteSurveyLanguage($input: DeleteSurveyLanguageInput!) {
    deleteSurveyLanguage(input: $input) {
      language
    }
  }
`);

export async function deleteSurveyLanguage(
  eventSlug: string,
  surveySlug: string,
  language: string,
) {
  await getClient().mutate({
    mutation: deleteSurveyLanguageMutation,
    variables: {
      input: {
        eventSlug,
        surveySlug,
        language,
      },
    },
  });
  revalidatePath(`/${eventSlug}/surveys`);
  redirect(`/${eventSlug}/surveys/${surveySlug}/edit`);
}
