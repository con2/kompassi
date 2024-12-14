import { PaymentStatus } from "@/__generated__/graphql";
import { ticketsBaseUrl } from "@/config";

export interface Order {
  orderNumber: number;
  formattedOrderNumber: string;
  status: PaymentStatus;
  createdAt: string;
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
  eventSlug: string,
  orderId: string,
): Promise<PayOrderResponse> {
  const response = await fetch(
    `${ticketsBaseUrl}/api/tickets-v2/${eventSlug}/orders/${orderId}/payment/`,
    { method: "POST" },
  );

  if (!response.ok) {
    const { detail } = await response.json();
    throw new Error(`Unexpected status code ${response.status}`, {
      cause: detail,
    });
  }

  return response.json();
}
