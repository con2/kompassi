"use server";

import { redirect } from "next/navigation";
import { revalidatePath } from "next/cache";
import { graphql } from "@/__generated__";
import {
  CancelAndRefundOrderInput,
  ResendOrderConfirmationInput,
  UpdateOrderInput,
  RefundType,
  FulfilOrderInput,
  PaymentStatus,
} from "@/__generated__/graphql";
import { getClient } from "@/apolloClient";

/// Another admin, or an automatic process, already acted on this order since
/// the caller's page was rendered. Bail out to a message rather than retrying
/// blindly on a premise that is no longer true.
const ORDER_STATE_CHANGED_MARKER = "no longer in the expected status";

function isOrderStateChanged(error: unknown): boolean {
  return (
    error instanceof Error && error.message.includes(ORDER_STATE_CHANGED_MARKER)
  );
}

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
  fromPaymentStatus: PaymentStatus,
) {
  const input: CancelAndRefundOrderInput = {
    eventSlug,
    orderId,
    refundType,
    fromPaymentStatus,
  };

  try {
    await getClient().mutate({
      mutation: refundOrderMutation,
      variables: { input },
    });
  } catch (error) {
    if (isOrderStateChanged(error)) {
      return void redirect(
        `/${eventSlug}/orders-admin/${orderId}?error=orderStateChanged`,
      );
    }
    throw error;
  }

  revalidatePath(`/${locale}/${eventSlug}/orders-admin/${orderId}`);
}

const fulfilOrderMutation = graphql(`
  mutation FulfilOrder($input: FulfilOrderInput!) {
    fulfilOrder(input: $input) {
      order {
        id
      }
    }
  }
`);

export async function fulfilOrder(
  locale: string,
  eventSlug: string,
  orderId: string,
  fromPaymentStatus: PaymentStatus,
) {
  const input: FulfilOrderInput = {
    eventSlug,
    orderId,
    fromPaymentStatus,
  };

  try {
    await getClient().mutate({
      mutation: fulfilOrderMutation,
      variables: { input },
    });
  } catch (error) {
    if (isOrderStateChanged(error)) {
      return void redirect(
        `/${eventSlug}/orders-admin/${orderId}?error=orderStateChanged`,
      );
    }
    throw error;
  }

  revalidatePath(`/${locale}/${eventSlug}/orders-admin/${orderId}`);
}
