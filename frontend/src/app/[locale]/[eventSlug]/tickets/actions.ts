"use server";

import { redirect } from "next/navigation";
import * as TicketsService from "./service";

export async function createOrder(
  locale: string,
  eventSlug: string,
  formData: FormData,
) {
  const order: TicketsService.CreateOrderRequest = {
    customer: {
      firstName: "" + (formData.get("firstName") ?? ""),
      lastName: "" + (formData.get("lastName") ?? ""),
      email: "" + (formData.get("email") ?? ""),
      phone: "" + (formData.get("phone") ?? ""),
    },
    products: Object.fromEntries(
      // NOTE: Array.from is a workaround for the following type error:
      // Property 'filter' does not exist on type 'IterableIterator<[string, FormDataEntryValue]>'.
      // Once Iterator.prototype.filter matures, we can remove Array.from.
      // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Iterator/filter
      Array.from(formData.entries())
        .filter(([key]) => key.startsWith("quantity-"))
        .map(
          ([key, value]) =>
            [key.replace("quantity-", ""), parseInt(value as string)] as const,
        )
        .filter(([_, quantity]) => quantity > 0),
    ),
    language: locale,
  };

  const response = await TicketsService.createOrder(eventSlug, order);

  if (response.success) {
    return void redirect(
      response.paymentRedirect || `/${eventSlug}/orders/${response.orderId}`,
    );
  } else {
    return void redirect(`/${eventSlug}/tickets/error?error=${response.error}`);
  }
}
