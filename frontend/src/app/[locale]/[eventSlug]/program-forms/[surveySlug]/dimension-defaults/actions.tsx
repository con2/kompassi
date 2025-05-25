"use server";

import { revalidatePath } from "next/cache";
import { graphql } from "@/__generated__";
import { getClient } from "@/apolloClient";

const mutation = graphql(`
  mutation UpdateProgramFormDefaultDimensions(
    $input: UpdateSurveyDefaultDimensionsInput!
  ) {
    updateSurveyDefaultDimensions(input: $input) {
      survey {
        slug
      }
    }
  }
`);

export async function updateProgramFormDefaultDimensions(
  locale: string,
  eventSlug: string,
  surveySlug: string,
  formData: FormData,
) {
  const input = {
    eventSlug,
    surveySlug,
    formData: Object.fromEntries(formData),
  };
  const { data } = await getClient().mutate({
    mutation,
    variables: { input },
  });
  revalidatePath(`/${locale}/${eventSlug}/program-forms`);
}
