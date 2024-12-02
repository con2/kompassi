import { ticketsBaseUrl } from "@/config";

export interface Order {
  products: {
    title: string;
    price: string;
    quantity: number;
  }[];
  total: string;
  status: "CONFIRMED" | "PAID" | "CANCELLED";
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
  const order = await response.json();
  return order;
}
