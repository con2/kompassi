"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";
import { graphql } from "@/__generated__";
import { getClient } from "@/apolloClient";
import { forceSlug } from "@/helpers/forceSlug";

const putDimensionMutation = graphql(`
  mutation PutSurveyDimension($input: PutDimensionInput!) {
    putDimension(input: $input) {
      dimension {
        slug
      }
    }
  }
`);

export async function createDimension(
  locale: string,
  scopeSlug: string,
  universeSlug: string,
  formData: FormData,
) {
  await getClient().mutate({
    mutation: putDimensionMutation,
    variables: {
      input: {
        scopeSlug,
        universeSlug,
        formData: forceSlug(Object.fromEntries(formData)),
      },
    },
  });
  revalidatePath(`/${locale}/${scopeSlug}/${universeSlug}`);

  redirect(`/${scopeSlug}/surveys/${universeSlug}/dimensions`);
}

export async function updateDimension(
  locale: string,
  scopeSlug: string,
  universeSlug: string,
  dimensionSlug: string,
  formData: FormData,
) {
  await getClient().mutate({
    mutation: putDimensionMutation,
    variables: {
      input: {
        scopeSlug,
        universeSlug,
        dimensionSlug,
        formData: forceSlug(Object.fromEntries(formData)),
      },
    },
  });
  revalidatePath(`/${locale}/${scopeSlug}/${universeSlug}`);

  redirect(`/${scopeSlug}/surveys/${universeSlug}/dimensions`);
}

export async function reorderDimensions(
  locale: string,
  scopeSlug: string,
  universeSlug: string,
  dimensionSlugs: string[],
) {
  // TODO(#565)
  console.log("reorderDimensions", scopeSlug, universeSlug, dimensionSlugs);
}

const deleteDimensionMutation = graphql(`
  mutation DeleteSurveyDimension($input: DeleteDimensionInput!) {
    deleteDimension(input: $input) {
      slug
    }
  }
`);

export async function deleteDimension(
  locale: string,
  scopeSlug: string,
  universeSlug: string,
  dimensionSlug: string,
) {
  await getClient().mutate({
    mutation: deleteDimensionMutation,
    variables: {
      input: {
        scopeSlug,
        universeSlug,
        dimensionSlug,
      },
    },
  });
  revalidatePath(`/${locale}/${scopeSlug}/${universeSlug}`);

  redirect(`/${scopeSlug}/surveys/${universeSlug}/dimensions`);
}

const putDimensionValueMutation = graphql(`
  mutation PutSurveyDimensionValue($input: PutDimensionValueInput!) {
    putDimensionValue(input: $input) {
      value {
        slug
      }
    }
  }
`);

export async function createDimensionValue(
  locale: string,
  scopeSlug: string,
  universeSlug: string,
  dimensionSlug: string,
  formData: FormData,
) {
  await getClient().mutate({
    mutation: putDimensionValueMutation,
    variables: {
      input: {
        scopeSlug,
        universeSlug,
        dimensionSlug,
        formData: forceSlug(Object.fromEntries(formData)),
      },
    },
  });
  revalidatePath(`/${locale}/${scopeSlug}/${universeSlug}`);

  redirect(`/${scopeSlug}/surveys/${universeSlug}/dimensions`);
}

export async function updateDimensionValue(
  locale: string,
  scopeSlug: string,
  universeSlug: string,
  dimensionSlug: string,
  valueSlug: string,
  formData: FormData,
) {
  await getClient().mutate({
    mutation: putDimensionValueMutation,
    variables: {
      input: {
        scopeSlug,
        universeSlug,
        dimensionSlug,
        valueSlug,
        formData: forceSlug(Object.fromEntries(formData)),
      },
    },
  });
  revalidatePath(`/${locale}/${scopeSlug}/${universeSlug}`);

  redirect(`/${scopeSlug}/surveys/${universeSlug}/dimensions`);
}

const deleteDimensionValueMutation = graphql(`
  mutation DeleteSurveyDimensionValue($input: DeleteDimensionValueInput!) {
    deleteDimensionValue(input: $input) {
      slug
    }
  }
`);

export async function deleteDimensionValue(
  locale: string,
  scopeSlug: string,
  universeSlug: string,
  dimensionSlug: string,
  valueSlug: string,
) {
  await getClient().mutate({
    mutation: deleteDimensionValueMutation,
    variables: {
      input: {
        scopeSlug,
        universeSlug,
        dimensionSlug,
        valueSlug,
      },
    },
  });
  revalidatePath(`/${locale}/${scopeSlug}/${universeSlug}`);

  redirect(`/${scopeSlug}/surveys/${universeSlug}/dimensions`);
}

export async function reorderDimensionValues(
  locale: string,
  scopeSlug: string,
  universeSlug: string,
  dimensionSlug: string,
  valueSlugs: string[],
) {
  // TODO(#565)
  console.log(
    "reorderDimensionValues",
    scopeSlug,
    universeSlug,
    dimensionSlug,
    valueSlugs,
  );
}
