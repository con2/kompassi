"use server";

import { revalidatePath } from "next/cache";
import { graphql } from "@/__generated__";
import { getClient } from "@/apolloClient";
import { Field } from "@/components/forms/models";

const mutation = graphql(`
  mutation UpdateFormFieldsMutation($input: UpdateFormFieldsInput!) {
    updateFormFields(input: $input) {
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
  fields: Field[],
) {
  const input = {
    eventSlug,
    surveySlug,
    language,
    fields,
  };

  await getClient().mutate({
    mutation: mutation,
    variables: {
      input,
    },
  });
  revalidatePath(`/events/${eventSlug}/surveys`);
}
