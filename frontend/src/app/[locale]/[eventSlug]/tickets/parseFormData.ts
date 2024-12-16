import { CreateOrderRequest } from "./service";

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
        [key.replace("quantity-", ""), parseInt(value as string, 10)] as const,
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
