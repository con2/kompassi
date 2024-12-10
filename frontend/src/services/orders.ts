import { ticketsBaseUrl } from "@/config";

export interface Order {
  orderNumber: number;
  status: "PENDING" | "PAID" | "CANCELLED";
  totalPrice: string;
  products: {
    title: string;
    price: string;
    quantity: number;
  }[];
}

export interface GetOrderResponse {
  event: {
    name: string;
  };
  order: Order;
}

export async function getOrder(
  eventSlug: string,
  orderId: string,
): Promise<GetOrderResponse> {
  const response = await fetch(
    `${ticketsBaseUrl}/api/tickets-v2/${eventSlug}/orders/${orderId}`,
  );
  return response.json();
}

interface PayOrderRequest {
  language: string;
  // provider: …
}

interface PayOrderResponse {
  paymentRedirect: string;
}

export async function payOrder(
  locale: string,
  eventSlug: string,
  orderId: string,
): Promise<PayOrderResponse> {
  const request: PayOrderRequest = {
    language: locale,
  };
  const response = await fetch(
    `${ticketsBaseUrl}/api/tickets-v2/${eventSlug}/orders/${orderId}/payment/`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(request),
    },
  );

  if (!response.ok) {
    throw new Error(`Unexpected status code ${response.status}`, {
      cause: response,
    });
  }

  return response.json();
}
