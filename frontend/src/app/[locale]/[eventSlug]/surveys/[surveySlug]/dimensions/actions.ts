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
  locale: string,
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
  revalidatePath(`/${locale}/${eventSlug}/${surveySlug}`);

  redirect(`/${eventSlug}/surveys/${surveySlug}/dimensions`);
}

export async function updateDimension(
  locale: string,
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
  revalidatePath(`/${locale}/${eventSlug}/${surveySlug}`);

  redirect(`/${eventSlug}/surveys/${surveySlug}/dimensions`);
}

export async function reorderDimensions(
  locale: string,
  eventSlug: string,
  surveySlug: string,
  dimensionSlugs: string[],
) {
  console.log("reorderDimensions", eventSlug, surveySlug, dimensionSlugs);
}

const deleteDimensionMutation = graphql(`
  mutation DeleteSurveyDimension($input: DeleteSurveyDimensionInput!) {
    deleteSurveyDimension(input: $input) {
      slug
    }
  }
`);

export async function deleteDimension(
  locale: string,
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
  revalidatePath(`/${locale}/${eventSlug}/${surveySlug}`);

  redirect(`/${eventSlug}/surveys/${surveySlug}/dimensions`);
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
  locale: string,
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
  revalidatePath(`/${locale}/${eventSlug}/${surveySlug}`);

  redirect(`/${eventSlug}/surveys/${surveySlug}/dimensions`);
}

export async function updateDimensionValue(
  locale: string,
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
  revalidatePath(`/${locale}/${eventSlug}/${surveySlug}`);

  redirect(`/${eventSlug}/surveys/${surveySlug}/dimensions`);
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
  locale: string,
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
  revalidatePath(`/${locale}/${eventSlug}/${surveySlug}`);

  redirect(`/${eventSlug}/surveys/${surveySlug}/dimensions`);
}

export async function reorderDimensionValues(
  locale: string,
  eventSlug: string,
  surveySlug: string,
  dimensionSlug: string,
  valueSlugs: string[],
) {
  console.log(
    "reorderDimensionValues",
    eventSlug,
    surveySlug,
    dimensionSlug,
    valueSlugs,
  );
}
