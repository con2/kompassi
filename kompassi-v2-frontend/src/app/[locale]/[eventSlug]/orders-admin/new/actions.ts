"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";
import { graphql } from "@/__generated__";
import { getClient } from "@/apolloClient";
import { parseFormData } from "@/services/tickets";

const mutation = graphql(`
  mutation AdminCreateOrder($input: CreateOrderInput!) {
    createOrder(input: $input) {
      order {
        event {
          slug
        }
        id
      }
    }
  }
`);

export async function adminCreateOrder(
  locale: string,
  eventSlug: string,
  formData: FormData,
): Promise<void> {
  const { customer, products, language } = parseFormData(
    formData,
    (formData.get("language") as string | undefined) || locale,
  );

  const input = {
    eventSlug,
    customer,
    language,
    products: Object.entries(products).map(([productId, quantity]) => ({
      productId: parseInt(productId, 10),
      quantity,
    })),
  };

  let orderId = "";

  try {
    const { data, errors } = await getClient().mutate({
      mutation,
      variables: { input },
    });

    if (errors) {
      console.error("GraphQL errors while creating order", { errors });
      return void redirect(
        `/${eventSlug}/orders-admin?error=failedToCreateOrder`,
      );
    } else if (!data?.createOrder?.order?.id) {
      console.error("No order id in GraphQL response", {
        input,
        data,
      });
      return void redirect(
        `/${eventSlug}/orders-admin?error=failedToCreateOrder`,
      );
    }

    eventSlug = data.createOrder.order.event.slug;
    orderId = data.createOrder.order.id;
  } catch (error) {
    console.error("Exception occurred while creating order", { error });
    return void redirect(
      `/${eventSlug}/orders-admin?error=failedToCreateOrder`,
    );
  }

  revalidatePath(`/${locale}/${eventSlug}/orders-admin`);
  redirect(`/${eventSlug}/orders-admin/${orderId}?success=orderCreated`);
}
