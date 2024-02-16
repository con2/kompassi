"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";
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
  revalidatePath(`/events/${eventSlug}/surveys`);
  redirect(`/events/${eventSlug}/surveys`);
}
