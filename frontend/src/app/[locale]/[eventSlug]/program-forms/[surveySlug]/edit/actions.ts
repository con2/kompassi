"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";
import { graphql } from "@/__generated__";
import { getClient } from "@/apolloClient";

const createProgramFormLanguageMutation = graphql(`
  mutation CreateProgramFormLanguage($input: CreateSurveyLanguageInput!) {
    createSurveyLanguage(input: $input) {
      form {
        language
      }
    }
  }
`);

export async function createProgramFormLanguage(
  eventSlug: string,
  surveySlug: string,
  formData: FormData,
) {
  const language = "" + formData.get("language");
  const copyFrom = formData.get("copyFrom");
  await getClient().mutate({
    mutation: createProgramFormLanguageMutation,
    variables: {
      input: {
        eventSlug,
        surveySlug,
        language,
        copyFrom: copyFrom ? "" + copyFrom : undefined,
      },
    },
  });
  revalidatePath(`/${eventSlug}/program-forms`);
  redirect(`/${eventSlug}/program-forms/${surveySlug}/edit/${language}`);
}

const updateProgramFormMutation = graphql(`
  mutation UpdateProgramFormMutation($input: UpdateSurveyInput!) {
    updateProgramForm(input: $input) {
      survey {
        slug
      }
    }
  }
`);

export async function updateProgramForm(
  eventSlug: string,
  surveySlug: string,
  formData: FormData,
) {
  await getClient().mutate({
    mutation: updateProgramFormMutation,
    variables: {
      input: {
        eventSlug,
        surveySlug,
        formData: Object.fromEntries(formData),
      },
    },
  });
  revalidatePath(`/${eventSlug}/surveys`);
}

const deleteProgramFormMutation = graphql(`
  mutation DeleteProrgamFormMutation($input: DeleteSurveyInput!) {
    deleteSurvey(input: $input) {
      slug
    }
  }
`);

export async function deleteProgramForm(eventSlug: string, surveySlug: string) {
  await getClient().mutate({
    mutation: deleteProgramFormMutation,
    variables: {
      input: {
        eventSlug,
        surveySlug,
      },
    },
  });
  revalidatePath(`/${eventSlug}/program-forms`);
  redirect(`/${eventSlug}/program-forms`);
}
