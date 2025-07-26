"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";
import { graphql } from "@/__generated__";
import { getClient } from "@/apolloClient";
import { forceSlug } from "@/helpers/forceSlug";

const universeSlug = "involvement";

const putDimensionMutation = graphql(`
  mutation PutInvolvementDimension($input: PutDimensionInput!) {
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
  const { slug: dimensionSlug, ...formData_ } = Object.fromEntries(formData);
  await getClient().mutate({
    mutation: putDimensionMutation,
    variables: {
      input: {
        scopeSlug,
        universeSlug,
        dimensionSlug: dimensionSlug as string,
        formData: formData_,
      },
    },
  });

  revalidatePath(`/${locale}/${scopeSlug}/involvement-dimensions`);
  redirect(`/${scopeSlug}/involvement-dimensions`);
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
        formData: forceSlug(Object.fromEntries(formData)),
      },
    },
  });

  revalidatePath(`/${locale}/${scopeSlug}/involvement-dimensions`);
  redirect(`/${scopeSlug}/involvement-dimensions`);
}

export async function reorderDimensions(
  locale: string,
  scopeSlug: string,
  dimensionSlugs: string[],
) {
  // TODO(#565)
  console.log("reorderDimensions", scopeSlug, universeSlug, dimensionSlugs);
}

const deleteDimensionMutation = graphql(`
  mutation DeleteInvolvementDimension($input: DeleteDimensionInput!) {
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

  revalidatePath(`/${locale}/${scopeSlug}/involvement-dimensions`);
  redirect(`/${scopeSlug}/involvement-dimensions`);
}

const putDimensionValueMutation = graphql(`
  mutation PutInvolvementDimensionValue($input: PutDimensionValueInput!) {
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
  const { slug: valueSlug, ...formData_ } = Object.fromEntries(formData);
  await getClient().mutate({
    mutation: putDimensionValueMutation,
    variables: {
      input: {
        scopeSlug,
        universeSlug,
        dimensionSlug,
        valueSlug: valueSlug as string,
        formData: formData_,
      },
    },
  });

  revalidatePath(`/${locale}/${scopeSlug}/involvement-dimensions`);
  redirect(`/${scopeSlug}/involvement-dimensions`);
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
        formData: forceSlug(Object.fromEntries(formData)),
      },
    },
  });

  revalidatePath(`/${locale}/${scopeSlug}/involvement-dimensions`);
  redirect(`/${scopeSlug}/involvement-dimensions`);
}

const deleteDimensionValueMutation = graphql(`
  mutation DeleteInvolvementDimensionValue($input: DeleteDimensionValueInput!) {
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

  revalidatePath(`/${locale}/${scopeSlug}/involvement-dimensions`);
  redirect(`/${scopeSlug}/involvement-dimensions`);
}

export async function reorderDimensionValues(
  locale: string,
  scopeSlug: string,
  dimensionSlug: string,
  valueSlugs: string[],
) {
  // TODO(#565)
  console.log("reorderDimensionValues", scopeSlug, dimensionSlug, valueSlugs);
}
