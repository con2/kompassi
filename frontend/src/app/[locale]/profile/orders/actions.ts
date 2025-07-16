"use server";
import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";
import { graphql } from "@/__generated__";
import { getClient } from "@/apolloClient";
import * as TicketService from "@/services/tickets";

const confirmEmailMutation = graphql(`
  mutation ConfirmEmail($input: ConfirmEmailInput!) {
    confirmEmail(input: $input) {
      user {
        email
      }
    }
  }
`);

export async function confirmEmail(locale: string) {
  let error = false;

  try {
    const { data } = await getClient().mutate({
      mutation: confirmEmailMutation,
      variables: { input: { locale } },
    });

    if (!data?.confirmEmail?.user?.email) {
      console.error("Email confirmation failed: No email returned");
      error = true;
    }
  } catch (error) {
    console.error("Error confirming email:", error);
    error = true;
  }

  if (error) {
    return void redirect(
      `/${locale}/profile/orders?error=emailConfirmationFailed`,
    );
  }

  revalidatePath(`/${locale}/profile/orders`);
  return void redirect(`/profile/orders?success=confirmationEmailSent`);
}

// TODO Redirect to profile order page instead of unauthenticated order page
export async function payOrder(
  locale: string,
  eventSlug: string,
  orderId: string,
) {
  const response = await TicketService.payOrder(eventSlug, orderId);
  revalidatePath(`/${locale}/${eventSlug}/orders/${orderId}`);
  return void redirect(response.paymentRedirect);
}
