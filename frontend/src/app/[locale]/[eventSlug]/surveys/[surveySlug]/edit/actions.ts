"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";
import { graphql } from "@/__generated__";
import { getClient } from "@/apolloClient";

const createSurveyLanguageMutation = graphql(`
  mutation CreateSurveyLanguage($input: CreateSurveyLanguageInput!) {
    createSurveyLanguage(input: $input) {
      form {
        language
      }
    }
  }
`);

export async function createSurveyLanguage(
  eventSlug: string,
  surveySlug: string,
  formData: FormData,
) {
  const language = "" + formData.get("language");
  const copyFrom = formData.get("copyFrom");
  await getClient().mutate({
    mutation: createSurveyLanguageMutation,
    variables: {
      input: {
        eventSlug,
        surveySlug,
        language,
        copyFrom: copyFrom ? "" + copyFrom : undefined,
      },
    },
  });
  revalidatePath(`/${eventSlug}/surveys`);
  redirect(`/${eventSlug}/surveys/${surveySlug}/edit/${language}`);
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
  revalidatePath(`/${eventSlug}/surveys`);
}

const deleteSurveyMutation = graphql(`
  mutation DeleteSurveyMutation($input: DeleteSurveyInput!) {
    deleteSurvey(input: $input) {
      slug
    }
  }
`);

export async function deleteSurvey(eventSlug: string, surveySlug: string) {
  await getClient().mutate({
    mutation: deleteSurveyMutation,
    variables: {
      input: {
        eventSlug,
        surveySlug,
      },
    },
  });
  revalidatePath(`/${eventSlug}/surveys`);
  redirect(`/${eventSlug}/surveys`);
}
