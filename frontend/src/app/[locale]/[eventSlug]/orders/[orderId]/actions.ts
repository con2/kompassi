"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";
import * as OrderService from "../../../../../services/orders";

export async function payOrder(
  locale: string,
  eventSlug: string,
  orderId: string,
) {
  const response = await OrderService.payOrder(locale, eventSlug);
  revalidatePath(`/${locale}/${eventSlug}/orders/${orderId}`);
  return void redirect(response.paymentRedirect);
}
