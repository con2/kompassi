import { PaymentStatus } from "@/__generated__/graphql";
import { ticketsApiKey, ticketsBaseUrl } from "@/config";
import {
  defaultLanguage,
  SupportedLanguage,
  supportedLanguages,
} from "@/translations";
import { validate as uuidValidate } from "uuid";

const headers = {
  "x-api-key": ticketsApiKey,
};

const postHeaders = {
  "content-type": "application/json",
  "x-api-key": ticketsApiKey,
};

const slugRegex = /^[a-z0-9-]+$/;
export function isValidSlug(slug: string): boolean {
  return slugRegex.test(slug);
}

export function isValidOrderId(orderId: string): boolean {
  return uuidValidate(orderId);
}

export interface Product {
  id: number;
  title: string;
  description: string;
  price: string;
  maxPerOrder: number;
  available?: boolean;
}

export interface GetProductsResponse {
  event: {
    name: string;
    termsAndConditionsUrl: string;
  };
  products: Product[];
}

export async function getProducts(
  locale: string,
  eventSlug: string,
): Promise<GetProductsResponse> {
  if (!supportedLanguages.includes(locale as SupportedLanguage)) {
    locale = defaultLanguage;
  }
  if (!isValidSlug(eventSlug)) {
    throw new Error(`Invalid event slug: ${eventSlug}`);
  }

  const url = `${ticketsBaseUrl}/api/tickets-v2/${eventSlug}/products/?language=${locale}`;
  const response = await fetch(url, { headers });
  if (response.ok) {
    return response.json();
  } else {
    throw new Error(`Unexpected status code ${response.status}`, {
      cause: await response.json(),
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
  language: string;
}

/// NOTE: custom form validation in ProductsForm relies on returning empty array when all quantities are zero
export function getProductEntries(
  formData: FormData,
): (readonly [string, number])[] {
  // NOTE: Array.from is a workaround for the following type error:
  // Property 'filter' does not exist on type 'IterableIterator<[string, FormDataEntryValue]>'.
  // Once Iterator.prototype.filter matures, we can remove Array.from.
  // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Iterator/filter
  return Array.from(formData.entries())
    .filter(([key]) => key.startsWith("quantity-"))
    .map(
      ([key, value]) =>
        [
          key.replace("quantity-", ""),
          !value ? 0 : parseInt(value as string, 10),
        ] as const,
    )
    .filter(([_, quantity]) => quantity > 0);
}

export function parseFormData(
  formData: FormData,
  locale: string,
): CreateOrderRequest {
  return {
    customer: {
      firstName: "" + (formData.get("firstName") ?? ""),
      lastName: "" + (formData.get("lastName") ?? ""),
      email: "" + (formData.get("email") ?? ""),
      phone: "" + (formData.get("phone") ?? ""),
    },
    products: Object.fromEntries(getProductEntries(formData)),
    language: locale,
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
  if (!isValidSlug(eventSlug)) {
    throw new Error(`Invalid event slug: ${eventSlug}`);
  }

  const response = await fetch(
    `${ticketsBaseUrl}/api/tickets-v2/${eventSlug}/orders/`,
    {
      method: "POST",
      headers: postHeaders,
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
  if (!isValidSlug(eventSlug)) {
    throw new Error(`Invalid event slug: ${eventSlug}`);
  }
  if (!isValidOrderId(orderId)) {
    throw new Error(`Invalid order ID: ${orderId}`);
  }

  const response = await fetch(
    `${ticketsBaseUrl}/api/tickets-v2/${eventSlug}/orders/${orderId}/`,
    { headers },
  );
  return response.json();
}

interface PayOrderResponse {
  paymentRedirect: string;
}

export async function payOrder(
  eventSlug: string,
  orderId: string,
): Promise<PayOrderResponse> {
  if (!isValidSlug(eventSlug)) {
    throw new Error(`Invalid event slug: ${eventSlug}`);
  }
  if (!isValidOrderId(orderId)) {
    throw new Error(`Invalid order ID: ${orderId}`);
  }

  const response = await fetch(
    `${ticketsBaseUrl}/api/tickets-v2/${eventSlug}/orders/${orderId}/payment/`,
    { method: "POST", headers: postHeaders },
  );

  if (!response.ok) {
    const { detail } = await response.json();
    throw new Error(`Unexpected status code ${response.status}`, {
      cause: detail,
    });
  }

  return response.json();
}
