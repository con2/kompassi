"use server";

import { revalidatePath } from "next/cache";

export async function resendConfirmation(
  locale: string,
  eventSlug: string,
  orderId: string,
) {
  console.log("resendConfirmation", locale, eventSlug, orderId);
  revalidatePath(`/${locale}/${eventSlug}/orders-admin/${orderId}`);
}

export async function updateContactInformation(
  locale: string,
  eventSlug: string,
  orderId: string,
  formData: FormData,
) {
  console.log("updateContactInformation", locale, eventSlug, orderId, formData);
  revalidatePath(`/${locale}/${eventSlug}/orders-admin/${orderId}`);
}

export async function cancelAndRefund(
  locale: string,
  eventSlug: string,
  orderId: string,
) {
  console.log("cancelAndRefund", locale, eventSlug, orderId);
  revalidatePath(`/${locale}/${eventSlug}/orders-admin/${orderId}`);
}

export async function cancelWithoutRefunding(
  locale: string,
  eventSlug: string,
  orderId: string,
) {
  console.log("cancelWithoutRefunding", locale, eventSlug, orderId);
  revalidatePath(`/${locale}/${eventSlug}/orders-admin/${orderId}`);
}
