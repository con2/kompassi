"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";
import { graphql } from "@/__generated__";
import { getClient } from "@/apolloClient";

const updateProgramFormLanguageMutation = graphql(`
  mutation UpdateProgramFormLanguage($input: UpdateFormInput!) {
    updateForm(input: $input) {
      survey {
        slug
      }
    }
  }
`);

export async function updateProgramFormLanguage(
  eventSlug: string,
  surveySlug: string,
  language: string,
  formData: FormData,
) {
  await getClient().mutate({
    mutation: updateProgramFormLanguageMutation,
    variables: {
      input: {
        eventSlug,
        surveySlug,
        language,
        formData: Object.fromEntries(formData),
      },
    },
  });
  revalidatePath(`/${eventSlug}/program-forms`);
}

const deleteProgramFormLanguageMutation = graphql(`
  mutation DeleteProgramFormLanguage($input: DeleteSurveyLanguageInput!) {
    deleteSurveyLanguage(input: $input) {
      language
    }
  }
`);

export async function deleteProgramFormLanguage(
  eventSlug: string,
  surveySlug: string,
  language: string,
) {
  await getClient().mutate({
    mutation: deleteProgramFormLanguageMutation,
    variables: {
      input: {
        eventSlug,
        surveySlug,
        language,
      },
    },
  });
  revalidatePath(`/${eventSlug}/program-forms`);
  redirect(`/${eventSlug}/program-forms/${surveySlug}/edit`);
}
