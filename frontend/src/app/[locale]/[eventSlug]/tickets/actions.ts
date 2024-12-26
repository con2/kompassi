"use server";

import { redirect } from "next/navigation";
import * as TicketService from "@/services/tickets";

export async function createOrder(
  locale: string,
  eventSlug: string,
  formData: FormData,
) {
  const order: TicketService.CreateOrderRequest = TicketService.parseFormData(
    formData,
    locale,
  );

  // If the user tried to make an all-zero order with JavaScript disabled, it would be caught here.
  // This is a fallback, as the form should prevent this from happening in the first place.
  if (Object.values(order.products).length === 0) {
    return void redirect(
      `/${eventSlug}/tickets/error?error=NO_PRODUCTS_SELECTED`,
    );
  }

  const response = await TicketService.createOrder(eventSlug, order);

  if (response.success) {
    return void redirect(
      response.paymentRedirect || `/${eventSlug}/orders/${response.orderId}`,
    );
  } else {
    return void redirect(`/${eventSlug}/tickets/error?error=${response.error}`);
  }
}
