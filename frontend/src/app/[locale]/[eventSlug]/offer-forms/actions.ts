"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";
import { graphql } from "@/__generated__";
import { getClient } from "@/apolloClient";

const createOfferFormMutation = graphql(`
  mutation CreateOfferForm($input: CreateSurveyInput!) {
    createOfferForm(input: $input) {
      survey {
        slug
      }
    }
  }
`);

export async function createOfferForm(eventSlug: string, formData: FormData) {
  const surveySlug = formData.get("slug")!.toString();

  await getClient().mutate({
    mutation: createOfferFormMutation,
    variables: { input: { eventSlug, surveySlug } },
  });

  revalidatePath(`/${eventSlug}/offer-forms`);
  redirect(`/${eventSlug}/offer-forms/${surveySlug}/edit`);
}
