"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";
import { graphql } from "@/__generated__";
import { getClient } from "@/apolloClient";

const createDimensionMutation = graphql(`
  mutation CreateSurveyDimension($input: CreateSurveyDimensionInput!) {
    createSurveyDimension(input: $input) {
      dimension {
        slug
      }
    }
  }
`);

export async function createDimension(
  eventSlug: string,
  surveySlug: string,
  formData: FormData,
) {
  await getClient().mutate({
    mutation: createDimensionMutation,
    variables: {
      input: {
        eventSlug,
        surveySlug,
        formData: Object.fromEntries(formData),
      },
    },
  });
  revalidatePath(`/events/${eventSlug}/surveys/${surveySlug}`);
  redirect(`/events/${eventSlug}/surveys/${surveySlug}/dimensions`);
}

export async function updateDimension(
  eventSlug: string,
  surveySlug: string,
  dimensionSlug: string,
  formData: FormData,
) {
  // TODO stubb
  console.log(
    "updateDimension",
    eventSlug,
    surveySlug,
    dimensionSlug,
    formData,
  );
}

export async function deleteDimension(
  eventSlug: string,
  surveySlug: string,
  dimensionSlug: string,
) {
  // TODO stubb
  console.log("deleteDimension", eventSlug, surveySlug, dimensionSlug);
}

export async function createDimensionValue(
  eventSlug: string,
  surveySlug: string,
  dimensionSlug: string,
  formData: FormData,
) {
  // TODO stubb
  console.log(
    "createDimensionValue",
    eventSlug,
    surveySlug,
    dimensionSlug,
    formData,
  );
}

export async function updateDimensionValue(
  eventSlug: string,
  surveySlug: string,
  dimensionSlug: string,
  valueSlug: string,
  formData: FormData,
) {
  // TODO stubb
  console.log(
    "updateDimensionValue",
    eventSlug,
    surveySlug,
    dimensionSlug,
    valueSlug,
    formData,
  );
}

export async function deleteDimensionValue(
  eventSlug: string,
  surveySlug: string,
  dimensionSlug: string,
  valueSlug: string,
) {
  // TODO stubb
  console.log(
    "deleteDimensionValue",
    eventSlug,
    surveySlug,
    dimensionSlug,
    valueSlug,
  );
}
