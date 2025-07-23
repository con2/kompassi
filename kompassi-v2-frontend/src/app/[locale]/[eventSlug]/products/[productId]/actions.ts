"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";
import { graphql } from "@/__generated__";
import { getClient } from "@/apolloClient";

const updateProductMutation = graphql(`
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
  productId: number,
  formData: FormData,
) {
  const result = await getClient().mutate({
    mutation: updateProductMutation,
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
    redirect(`/${eventSlug}/products/${newProductId}`);
  }
}

const deleteProductMutation = graphql(`
  mutation DeleteProduct($input: DeleteProductInput!) {
    deleteProduct(input: $input) {
      id
    }
  }
`);

export async function deleteProduct(
  locale: string,
  eventSlug: string,
  productId: string,
) {
  try {
    await getClient().mutate({
      mutation: deleteProductMutation,
      variables: {
        input: {
          eventSlug,
          productId,
        },
      },
    });
  } catch (error: any) {
    console.error(await error.response.json());
  }

  revalidatePath(`/${locale}/${eventSlug}/products`);
  redirect(`/${eventSlug}/products`);
}
