"use server";

import { revalidatePath } from "next/cache";

export async function updateProduct(
  locale: string,
  eventSlug: string,
  productId: string,
  formData: FormData,
) {
  console.log("updateProduct", locale, eventSlug, productId, formData);
  revalidatePath(`/${locale}/${eventSlug}/products/${productId}`);
}
