"use server";

import { revalidatePath } from "next/cache";
import { graphql } from "@/__generated__";
import {
  CancelAndRefundOrderInput,
  ResendOrderConfirmationInput,
  UpdateOrderInput,
  RefundType,
  MarkOrderAsPaidInput,
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
  mutation CancelAndRefundOrder($input: CancelAndRefundOrderInput!) {
    cancelAndRefundOrder(input: $input) {
      order {
        id
      }
    }
  }
`);

export async function cancelAndRefundOrder(
  locale: string,
  eventSlug: string,
  orderId: string,
  refundType: RefundType,
) {
  const input: CancelAndRefundOrderInput = {
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

const markOrderAsPaidMutation = graphql(`
  mutation MarkOrderAsPaid($input: MarkOrderAsPaidInput!) {
    markOrderAsPaid(input: $input) {
      order {
        id
      }
    }
  }
`);

export async function markOrderAsPaid(
  locale: string,
  eventSlug: string,
  orderId: string,
) {
  const input: MarkOrderAsPaidInput = {
    eventSlug,
    orderId,
  };

  await getClient().mutate({
    mutation: markOrderAsPaidMutation,
    variables: { input },
  });

  revalidatePath(`/${locale}/${eventSlug}/orders-admin/${orderId}`);
}
