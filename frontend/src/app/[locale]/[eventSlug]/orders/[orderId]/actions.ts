"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";
import * as TicketService from "../../../../../services/tickets";
import { graphql } from "@/__generated__/gql";
import { getClient } from "@/apolloClient";

export async function payOrder(
  locale: string,
  eventSlug: string,
  orderId: string,
) {
  const response = await TicketService.payOrder(eventSlug, orderId);
  revalidatePath(`/${locale}/${eventSlug}/orders/${orderId}`);
  return void redirect(response.paymentRedirect);
}

const cancelOwnOrderMutation = graphql(`
  mutation CancelOwnOrder($input: CancelOwnUnpaidOrderInput!) {
    cancelOwnUnpaidOrder(input: $input) {
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
  const response = await getClient().mutate({
    mutation: cancelOwnOrderMutation,
    variables: {
      input: {
        eventSlug,
        orderId,
      },
    },
  });

  if (response.data?.cancelOwnUnpaidOrder?.order) {
    revalidatePath(`/${locale}/${eventSlug}/orders/${orderId}`);
    return void redirect(`/${eventSlug}/orders/${orderId}?success=cancelled`);
  } else {
    return void redirect(
      `/${eventSlug}/orders/${orderId}?error=failedToCancel`,
    );
  }
}
