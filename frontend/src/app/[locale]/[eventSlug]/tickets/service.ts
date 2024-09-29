import { kompassiBaseUrl } from "@/config";

export interface Product {
  id: number;
  title: string;
  description: string;
  price: string;
  available: boolean;
}

export interface GetProductsResponse {
  event: {
    name: string;
  };
  products: Product[];
}

export async function getProducts(
  eventSlug: string,
): Promise<GetProductsResponse> {
  const response = await fetch(
    `${kompassiBaseUrl}/api/tickets-v2/${eventSlug}/products/`,
  );
  const products = await response.json();
  return products;
}
