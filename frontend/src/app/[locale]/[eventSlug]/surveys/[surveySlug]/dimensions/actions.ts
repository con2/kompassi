"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";
import { graphql } from "@/__generated__";
import { getClient } from "@/apolloClient";

const putDimensionMutation = graphql(`
  mutation PutSurveyDimension($input: PutSurveyDimensionInput!) {
    putSurveyDimension(input: $input) {
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
    mutation: putDimensionMutation,
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
  await getClient().mutate({
    mutation: putDimensionMutation,
    variables: {
      input: {
        eventSlug,
        surveySlug,
        dimensionSlug,
        formData: Object.fromEntries(formData),
      },
    },
  });
  revalidatePath(`/events/${eventSlug}/surveys/${surveySlug}`);
  redirect(`/events/${eventSlug}/surveys/${surveySlug}/dimensions`);
}

const deleteDimensionMutation = graphql(`
  mutation DeleteSurveyDimension($input: DeleteSurveyDimensionInput!) {
    deleteSurveyDimension(input: $input) {
      slug
    }
  }
`);

export async function deleteDimension(
  eventSlug: string,
  surveySlug: string,
  dimensionSlug: string,
) {
  await getClient().mutate({
    mutation: deleteDimensionMutation,
    variables: {
      input: {
        eventSlug,
        surveySlug,
        dimensionSlug,
      },
    },
  });
  revalidatePath(`/events/${eventSlug}/surveys/${surveySlug}`);
  redirect(`/events/${eventSlug}/surveys/${surveySlug}/dimensions`);
}

const putDimensionValueMutation = graphql(`
  mutation PutSurveyDimensionValue($input: PutSurveyDimensionValueInput!) {
    putSurveyDimensionValue(input: $input) {
      value {
        slug
      }
    }
  }
`);

export async function createDimensionValue(
  eventSlug: string,
  surveySlug: string,
  dimensionSlug: string,
  formData: FormData,
) {
  await getClient().mutate({
    mutation: putDimensionValueMutation,
    variables: {
      input: {
        eventSlug,
        surveySlug,
        dimensionSlug,
        formData: Object.fromEntries(formData),
      },
    },
  });
  revalidatePath(`/events/${eventSlug}/surveys/${surveySlug}`);
  redirect(`/events/${eventSlug}/surveys/${surveySlug}/dimensions`);
}

export async function updateDimensionValue(
  eventSlug: string,
  surveySlug: string,
  dimensionSlug: string,
  valueSlug: string,
  formData: FormData,
) {
  await getClient().mutate({
    mutation: putDimensionValueMutation,
    variables: {
      input: {
        eventSlug,
        surveySlug,
        dimensionSlug,
        valueSlug,
        formData: Object.fromEntries(formData),
      },
    },
  });
  revalidatePath(`/events/${eventSlug}/surveys/${surveySlug}`);
  redirect(`/events/${eventSlug}/surveys/${surveySlug}/dimensions`);
}

const deleteDimensionValueMutation = graphql(`
  mutation DeleteSurveyDimensionValue(
    $input: DeleteSurveyDimensionValueInput!
  ) {
    deleteSurveyDimensionValue(input: $input) {
      slug
    }
  }
`);

export async function deleteDimensionValue(
  eventSlug: string,
  surveySlug: string,
  dimensionSlug: string,
  valueSlug: string,
) {
  await getClient().mutate({
    mutation: deleteDimensionValueMutation,
    variables: {
      input: {
        eventSlug,
        surveySlug,
        dimensionSlug,
        valueSlug,
      },
    },
  });
  revalidatePath(`/events/${eventSlug}/surveys/${surveySlug}`);
  redirect(`/events/${eventSlug}/surveys/${surveySlug}/dimensions`);
}
