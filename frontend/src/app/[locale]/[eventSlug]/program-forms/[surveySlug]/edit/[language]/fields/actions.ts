"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";
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
  revalidatePath(`/${eventSlug}/surveys`);
}

const promoteFieldToDimensionMutation = graphql(`
  mutation PromoteProgramFormFieldToDimension(
    $input: PromoteFieldToDimensionInput!
  ) {
    promoteFieldToDimension(input: $input) {
      survey {
        slug
      }
    }
  }
`);

export async function promoteFieldToDimension(
  locale: string,
  eventSlug: string,
  surveySlug: string,
  fieldSlug: string,
) {
  await getClient().mutate({
    mutation: promoteFieldToDimensionMutation,
    variables: {
      input: {
        eventSlug,
        surveySlug,
        fieldSlug,
      },
    },
  });
  revalidatePath(`/${locale}/${eventSlug}/program-forms`);
  revalidatePath(`/${locale}/${eventSlug}/program-dimensions`);
  redirect(`/${eventSlug}/program-dimensions`);
}
