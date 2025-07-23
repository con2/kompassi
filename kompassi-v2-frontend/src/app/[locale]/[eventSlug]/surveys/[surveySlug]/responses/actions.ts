"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";
import { graphql } from "@/__generated__";
import { getClient } from "@/apolloClient";

const subscribeToSurveyResponses = graphql(`
  mutation SubscribeToSurveyResponses($input: SubscriptionInput!) {
    subscribeToSurveyResponses(input: $input) {
      success
    }
  }
`);

const unsubscribeFromSurveyResponses = graphql(`
  mutation UnsubscribeFromSurveyResponses($input: SubscriptionInput!) {
    unsubscribeFromSurveyResponses(input: $input) {
      success
    }
  }
`);

export async function toggleSurveyResponseSubscription(
  locale: string,
  eventSlug: string,
  surveySlug: string,
  subscribe: boolean,
): Promise<void> {
  const mutation = subscribe
    ? subscribeToSurveyResponses
    : unsubscribeFromSurveyResponses;
  await getClient().mutate({
    mutation,
    variables: { input: { eventSlug, surveySlug } },
  });
  revalidatePath(`/${locale}/${eventSlug}/surveys/${surveySlug}/responses`);
}

const deleteSurveyResponsesMutation = graphql(`
  mutation DeleteSurveyResponses($input: DeleteSurveyResponsesInput!) {
    deleteSurveyResponses(input: $input) {
      countDeleted
    }
  }
`);

export async function deleteSurveyResponses(
  locale: string,
  eventSlug: string,
  surveySlug: string,
  responseIds: string[],
  searchParams: Record<string, string>,
): Promise<void> {
  await getClient().mutate({
    mutation: deleteSurveyResponsesMutation,
    variables: {
      input: {
        eventSlug,
        surveySlug,
        responseIds,
      },
    },
  });
  revalidatePath(`/${locale}/${eventSlug}/surveys/${surveySlug}/responses`);

  const queryString =
    Object.entries(searchParams).length > 0
      ? "?" + new URLSearchParams(searchParams).toString()
      : "";

  redirect(`/${eventSlug}/surveys/${surveySlug}/responses${queryString}`);
}
