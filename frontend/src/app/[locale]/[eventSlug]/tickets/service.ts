import { ticketsBaseUrl } from "@/config";

export interface GetProductsResponse {
  event: {
    name: string;
  };
  products: {
    id: number;
    title: string;
    description: string;
    price: string;
    available?: boolean;
  }[];
}

export async function getProducts(
  eventSlug: string,
): Promise<GetProductsResponse> {
  const url = `${ticketsBaseUrl}/api/tickets-v2/${eventSlug}/products/`;
  const response = await fetch(url);
  if (response.ok) {
    return response.json();
  } else {
    throw new Error(`Unexpected status code ${response.status}`, {
      cause: response,
    });
  }
}

export interface CreateOrderRequest {
  customer: {
    firstName: string;
    lastName: string;
    email: string;
    phone?: string;
  };
  products: {
    [productId: string]: number;
  };
}

export interface SuccessfulOrderResponse {
  success: true;
  orderId: string; // UUID
  paymentRedirect?: string;
}

export interface FailedOrderResponse {
  success: false;
  error: "NOT_ENOUGH_TICKETS" | "INVALID_ORDER" | "UNKNOWN_ERROR";
}

export type OrderResponse = SuccessfulOrderResponse | FailedOrderResponse;

export async function createOrder(
  eventSlug: string,
  order: CreateOrderRequest,
): Promise<OrderResponse> {
  const response = await fetch(
    `${ticketsBaseUrl}/api/tickets-v2/${eventSlug}/orders/`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(order),
    },
  );

  switch (response.status) {
    case 200:
    case 201:
      const { orderId, paymentRedirect } = await response.json();
      return { success: true, orderId, paymentRedirect };
    case 400:
    case 409:
      const { detail } = await response.json();
      return { success: false, error: detail ?? "UNKNOWN_ERROR" };
    default:
      throw new Error(`Unexpected status code ${response.status}`, {
        cause: response,
      });
  }
}
