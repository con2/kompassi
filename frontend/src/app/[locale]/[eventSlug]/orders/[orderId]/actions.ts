"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";
import * as TicketService from "../../../../../services/tickets";

export async function payOrder(
  locale: string,
  eventSlug: string,
  orderId: string,
) {
  const response = await TicketService.payOrder(eventSlug, orderId);
  revalidatePath(`/${locale}/${eventSlug}/orders/${orderId}`);
  return void redirect(response.paymentRedirect);
}
