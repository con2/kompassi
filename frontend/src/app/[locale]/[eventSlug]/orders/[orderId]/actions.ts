"use server";

import { redirect } from "next/navigation";
import * as OrderService from "./service";

export async function payOrder(
  locale: string,
  eventSlug: string,
  orderId: string,
) {
  const response = await OrderService.payOrder(locale, eventSlug, orderId);
  return void redirect(response.paymentRedirect);
}
