"use server";

import { revalidatePath } from "next/cache";
import { graphql } from "@/__generated__";
import {
  CancelOrderInput,
  RefundOrderInput,
  ResendOrderConfirmationInput,
  UpdateOrderInput,
  RefundType,
} from "@/__generated__/graphql";
import { getClient } from "@/apolloClient";

const resendConfirmationMutation = graphql(`
  mutation ResendOrderConfirmation($input: ResendOrderConfirmationInput!) {
    resendOrderConfirmation(input: $input) {
      order {
        id
      }
    }
  }
`);

export async function resendConfirmation(
  locale: string,
  eventSlug: string,
  orderId: string,
) {
  const input: ResendOrderConfirmationInput = {
    eventSlug,
    orderId,
  };

  await getClient().mutate({
    mutation: resendConfirmationMutation,
    variables: { input },
  });

  revalidatePath(`/${locale}/${eventSlug}/orders-admin/${orderId}`);
}

const updateOrderMutation = graphql(`
  mutation UpdateOrder($input: UpdateOrderInput!) {
    updateOrder(input: $input) {
      order {
        id
      }
    }
  }
`);

export async function updateOrder(
  locale: string,
  eventSlug: string,
  orderId: string,
  formData: FormData,
) {
  const input: UpdateOrderInput = {
    eventSlug,
    orderId,
    formData: Object.fromEntries(formData),
  };

  await getClient().mutate({
    mutation: updateOrderMutation,
    variables: { input },
  });

  revalidatePath(`/${locale}/${eventSlug}/orders-admin/${orderId}`);
}

const refundOrderMutation = graphql(`
  mutation RefundOrder($input: RefundOrderInput!) {
    refundOrder(input: $input) {
      order {
        id
      }
    }
  }
`);

export async function refundOrder(
  locale: string,
  eventSlug: string,
  orderId: string,
  refundType: RefundType,
) {
  const input: RefundOrderInput = {
    eventSlug,
    orderId,
    refundType,
  };

  await getClient().mutate({
    mutation: refundOrderMutation,
    variables: { input },
  });

  revalidatePath(`/${locale}/${eventSlug}/orders-admin/${orderId}`);
}

const cancelOrderMutation = graphql(`
  mutation CancelOrder($input: CancelOrderInput!) {
    cancelOrder(input: $input) {
      order {
        id
      }
    }
  }
`);

export async function cancelOrder(
  locale: string,
  eventSlug: string,
  orderId: string,
) {
  const input: CancelOrderInput = {
    eventSlug,
    orderId,
  };

  await getClient().mutate({
    mutation: cancelOrderMutation,
    variables: { input },
  });

  revalidatePath(`/${locale}/${eventSlug}/orders-admin/${orderId}`);
}
