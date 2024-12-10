"use server";
import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";
import * as OrderService from "@/services/orders";

export async function confirmEmail(locale: string) {
  console.log("confirmEmail", locale);
}

// TODO Redirect to profile order page instead of unauthenticated order page
export async function payOrder(
  locale: string,
  eventSlug: string,
  orderId: string,
) {
  const response = await OrderService.payOrder(locale, eventSlug, orderId);
  revalidatePath(`/${locale}/${eventSlug}/orders/${orderId}`);
  return void redirect(response.paymentRedirect);
}
