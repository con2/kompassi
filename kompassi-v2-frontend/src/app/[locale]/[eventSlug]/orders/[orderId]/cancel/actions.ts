"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";
import { graphql } from "@/__generated__/gql";
import { getClient } from "@/apolloClient";

const requestOrderCancellationMutation = graphql(`
  mutation RequestOrderCancellation($input: RequestOrderCancellationInput!) {
    requestOrderCancellation(input: $input) {
      success
    }
  }
`);

export async function requestOrderCancellation(
  locale: string,
  eventSlug: string,
  orderId: string,
) {
  let success = false;
  try {
    const response = await getClient().mutate({
      mutation: requestOrderCancellationMutation,
      variables: {
        input: {
          eventSlug,
          orderId,
        },
      },
    });
    success = !!response.data?.requestOrderCancellation?.success;
  } catch (error) {
    console.error("requestOrderCancellation failed", error);
  }

  if (success) {
    return void redirect(
      `/${eventSlug}/orders/${orderId}/cancel?success=cancellationRequested`,
    );
  } else {
    return void redirect(
      `/${eventSlug}/orders/${orderId}/cancel?error=cancellationRequestFailed`,
    );
  }
}

const confirmOrderCancellationMutation = graphql(`
  mutation ConfirmOrderCancellation($input: ConfirmOrderCancellationInput!) {
    confirmOrderCancellation(input: $input) {
      success
    }
  }
`);

export async function confirmOrderCancellation(
  locale: string,
  eventSlug: string,
  orderId: string,
  code: string,
) {
  // "cancelled": order cancelled, refund (if any) initiated
  // "refundFailed": order cancelled, but the provider rejected the refund request
  // "error": nothing happened (eg. invalid or expired code)
  let outcome: "cancelled" | "refundFailed" | "error" = "error";
  try {
    const response = await getClient().mutate({
      mutation: confirmOrderCancellationMutation,
      variables: {
        input: {
          eventSlug,
          orderId,
          code,
        },
      },
    });
    if (response.data?.confirmOrderCancellation) {
      outcome = response.data.confirmOrderCancellation.success
        ? "cancelled"
        : "refundFailed";
    }
  } catch (error) {
    console.error("confirmOrderCancellation failed", error);
  }

  switch (outcome) {
    case "cancelled":
      revalidatePath(`/${locale}/${eventSlug}/orders/${orderId}`);
      return void redirect(`/${eventSlug}/orders/${orderId}?success=cancelled`);
    case "refundFailed":
      revalidatePath(`/${locale}/${eventSlug}/orders/${orderId}`);
      return void redirect(
        `/${eventSlug}/orders/${orderId}?error=refundFailed`,
      );
    default:
      return void redirect(
        `/${eventSlug}/orders/${orderId}/cancel/${code}?error=cancellationFailed`,
      );
  }
}
