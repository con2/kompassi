"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";
import { graphql } from "@/__generated__";
import { getClient } from "@/apolloClient";

const mutation = graphql(`
  mutation UpdateProduct($input: UpdateProductInput!) {
    updateProduct(input: $input) {
      product {
        id
      }
    }
  }
`);

export async function updateProduct(
  locale: string,
  eventSlug: string,
  productId: string,
  formData: FormData,
) {
  console.log({
    eventSlug,
    productId,
    formData,
  });
  const result = await getClient().mutate({
    mutation,
    variables: {
      input: {
        eventSlug,
        productId,
        formData: Object.fromEntries(formData),
      },
    },
  });

  revalidatePath(`/${locale}/${eventSlug}/products/${productId}`);
  revalidatePath(`/${locale}/${eventSlug}/products`);

  // id may have changed due to new revision
  const newProductId = result.data?.updateProduct?.product?.id;
  if (productId !== newProductId) {
    redirect(`/${locale}/${eventSlug}/products/${newProductId}`);
  }
}
