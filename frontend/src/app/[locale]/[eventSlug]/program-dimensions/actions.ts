"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";
import { graphql } from "@/__generated__";
import { getClient } from "@/apolloClient";

const universeSlug = "program";

const putDimensionMutation = graphql(`
  mutation PutProgramDimension($input: PutDimensionInput!) {
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
  formData: FormData,
) {
  await getClient().mutate({
    mutation: putDimensionMutation,
    variables: {
      input: {
        scopeSlug,
        universeSlug,
        formData: Object.fromEntries(formData),
      },
    },
  });

  revalidatePath(`/${locale}/${scopeSlug}/program-dimensions`);
  redirect(`/${scopeSlug}/program-dimensions`);
}

export async function updateDimension(
  locale: string,
  scopeSlug: string,
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
        formData: Object.fromEntries(formData),
      },
    },
  });

  revalidatePath(`/${locale}/${scopeSlug}/program-dimensions`);
  redirect(`/${scopeSlug}/program-dimensions`);
}

export async function reorderDimensions(
  locale: string,
  scopeSlug: string,
  dimensionSlugs: string[],
) {
  console.log("reorderDimensions", scopeSlug, universeSlug, dimensionSlugs);
}

const deleteDimensionMutation = graphql(`
  mutation DeleteProgramDimension($input: DeleteDimensionInput!) {
    deleteDimension(input: $input) {
      slug
    }
  }
`);

export async function deleteDimension(
  locale: string,
  scopeSlug: string,
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

  revalidatePath(`/${locale}/${scopeSlug}/program-dimensions`);
  redirect(`/${scopeSlug}/program-dimensions`);
}

const putDimensionValueMutation = graphql(`
  mutation PutProgramDimensionValue($input: PutDimensionValueInput!) {
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
        formData: Object.fromEntries(formData),
      },
    },
  });

  revalidatePath(`/${locale}/${scopeSlug}/program-dimensions`);
  redirect(`/${scopeSlug}/program-dimensions`);
}

export async function updateDimensionValue(
  locale: string,
  scopeSlug: string,
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
        formData: Object.fromEntries(formData),
      },
    },
  });

  revalidatePath(`/${locale}/${scopeSlug}/program-dimensions`);
  redirect(`/${scopeSlug}/program-dimensions`);
}

const deleteDimensionValueMutation = graphql(`
  mutation DeleteProgramDimensionValue($input: DeleteDimensionValueInput!) {
    deleteDimensionValue(input: $input) {
      slug
    }
  }
`);

export async function deleteDimensionValue(
  locale: string,
  scopeSlug: string,
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

  revalidatePath(`/${locale}/${scopeSlug}/program-dimensions`);
  redirect(`/${scopeSlug}/program-dimensions`);
}

export async function reorderDimensionValues(
  locale: string,
  scopeSlug: string,
  dimensionSlug: string,
  valueSlugs: string[],
) {
  console.log("reorderDimensionValues", scopeSlug, dimensionSlug, valueSlugs);
}
