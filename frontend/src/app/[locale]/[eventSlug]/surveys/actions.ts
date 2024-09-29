"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";
import { graphql } from "@/__generated__";
import { getClient } from "@/apolloClient";

const createSurveyMutation = graphql(`
  mutation CreateSurvey($input: CreateSurveyInput!) {
    createSurvey(input: $input) {
      survey {
        slug
      }
    }
  }
`);

export async function createSurvey(eventSlug: string, formData: FormData) {
  const surveySlug = formData.get("slug")!.toString();

  await getClient().mutate({
    mutation: createSurveyMutation,
    variables: { input: { eventSlug, surveySlug } },
  });

  revalidatePath(`/events/${eventSlug}/surveys`);
  redirect(`/events/${eventSlug}/surveys/${surveySlug}/edit`);
}
