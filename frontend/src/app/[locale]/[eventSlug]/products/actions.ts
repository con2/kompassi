"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";
import { graphql } from "@/__generated__";
import { getClient } from "@/apolloClient";

const mutation = graphql(`
  mutation CreateProduct($input: CreateProductInput!) {
    createProduct(input: $input) {
      product {
        id
      }
    }
  }
`);

export async function createProduct(
  locale: string,
  eventSlug: string,
  formData: FormData,
) {
  const result = await getClient().mutate({
    mutation,
    variables: {
      input: {
        eventSlug,
        formData: Object.fromEntries(formData),
      },
    },
  });

  revalidatePath(`/${locale}/${eventSlug}/products`);

  const newProductId = result.data?.createProduct?.product?.id;
  redirect(`/${eventSlug}/products/${newProductId ?? ""}`);
}
