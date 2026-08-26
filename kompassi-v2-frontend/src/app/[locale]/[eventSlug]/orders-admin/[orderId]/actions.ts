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
import { getClient, graphqlErrorCode } from "@/apolloClient";

/// Refusals the order state machine reports with a machine-readable
/// extensions.code (see kompassi/tickets_v2/graphql/errors.py), mapped to the
/// `?error=` key whose message Tickets.admin.messages carries.
///
/// ORDER_STATE_CHANGED: another admin, or an automatic process, already acted on
/// this order since the caller's page was rendered.
/// TICKETS_UNAVAILABLE: the order could not be given the tickets it is owed, and
/// nothing was changed.
const errorMessageByCode: Record<string, string> = {
  ORDER_STATE_CHANGED: "orderStateChanged",
  TICKETS_UNAVAILABLE: "ticketsUnavailable",
};

/// Fallback for a backend older than the error codes: the prose of
/// OrderStateChanged. Kept only so a version skew degrades to the right message
/// rather than an unhandled 500.
const orderStateChangedMarker = "no longer in the expected status";

/// Returns the `?error=` key to bail out to, or undefined to rethrow.
function orderErrorKey(error: unknown): string | undefined {
  const code = graphqlErrorCode(error);
  if (code && errorMessageByCode[code]) {
    return errorMessageByCode[code];
  }

  if (
    error instanceof Error &&
    error.message.includes(orderStateChangedMarker)
  ) {
    return "orderStateChanged";
  }

  return undefined;
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
    const errorKey = orderErrorKey(error);
    if (errorKey) {
      return void redirect(
        `/${eventSlug}/orders-admin/${orderId}?error=${errorKey}`,
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
    const errorKey = orderErrorKey(error);
    if (errorKey) {
      return void redirect(
        `/${eventSlug}/orders-admin/${orderId}?error=${errorKey}`,
      );
    }
    throw error;
  }

  revalidatePath(`/${locale}/${eventSlug}/orders-admin/${orderId}`);
}
