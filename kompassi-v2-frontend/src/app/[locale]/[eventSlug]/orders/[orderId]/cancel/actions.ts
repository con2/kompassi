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
  let success = false;
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
    success = !!response.data?.confirmOrderCancellation?.success;
  } catch (error) {
    console.error("confirmOrderCancellation failed", error);
  }

  if (success) {
    revalidatePath(`/${locale}/${eventSlug}/orders/${orderId}`);
    return void redirect(`/${eventSlug}/orders/${orderId}?success=cancelled`);
  } else {
    return void redirect(
      `/${eventSlug}/orders/${orderId}/cancel/${code}?error=cancellationFailed`,
    );
  }
}
