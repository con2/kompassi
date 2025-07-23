"use server";

import { revalidatePath } from "next/cache";
import { graphql } from "@/__generated__";
import { SurveyDefaultDimensionsUniverse } from "@/__generated__/graphql";
import { getClient } from "@/apolloClient";

const mutation = graphql(`
  mutation UpdateSurveyDefaultDimensions(
    $input: UpdateSurveyDefaultDimensionsInput!
  ) {
    updateSurveyDefaultDimensions(input: $input) {
      survey {
        slug
      }
    }
  }
`);

export async function updateSurveyDefaultDimensions(
  locale: string,
  eventSlug: string,
  surveySlug: string,
  formData: FormData,
) {
  const input = {
    eventSlug,
    surveySlug,
    universe: SurveyDefaultDimensionsUniverse.Response, // TODO Involvement too
    formData: Object.fromEntries(formData),
  };
  await getClient().mutate({
    mutation,
    variables: { input },
  });
  revalidatePath(`/${locale}/${eventSlug}/surveys/${surveySlug}`);
}
