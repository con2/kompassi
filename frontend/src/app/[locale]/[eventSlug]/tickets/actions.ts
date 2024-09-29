"use server";

import { Order } from "./models";
import { kompassiBaseUrl } from "@/config";

export async function createOrder(
  locale: string,
  eventSlug: string,
  formData: FormData,
) {
  console.log(formData);
  const order: Order = {
    customer: {
      firstName: "" + (formData.get("firstName") ?? ""),
      lastName: "" + (formData.get("lastName") ?? ""),
      email: "" + (formData.get("email") ?? ""),
      phone: "" + (formData.get("phone") ?? ""),
    },
    products: Object.fromEntries(
      Object.entries(formData)
        .filter(([key]) => key.startsWith("quantity-"))
        .map(([key, value]) => [
          key.replace("quantity-", ""),
          parseInt(value as string),
        ]),
    ),
  };

  console.log({ order });
  const response = await fetch(
    `${kompassiBaseUrl}/api/tickets-v2/events/${eventSlug}/orders/`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(order),
    },
  );
}
