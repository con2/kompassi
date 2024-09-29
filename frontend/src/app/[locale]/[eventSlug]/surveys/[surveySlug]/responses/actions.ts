"use server";

import { revalidatePath } from "next/cache";
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
