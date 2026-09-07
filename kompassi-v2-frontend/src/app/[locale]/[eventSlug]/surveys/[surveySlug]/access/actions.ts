"use server";

import { revalidatePath } from "next/cache";
import { graphql } from "@/__generated__";
import { getClient } from "@/apolloClient";

const grantSurveyAccessMutation = graphql(`
  mutation GrantSurveyAccess($input: SurveyAccessInput!) {
    grantSurveyAccess(input: $input) {
      survey {
        slug
      }
    }
  }
`);

export async function grantSurveyAccess(
  locale: string,
  eventSlug: string,
  surveySlug: string,
  formData: FormData,
) {
  const personId = parseInt("" + formData.get("personId"), 10);

  await getClient().mutate({
    mutation: grantSurveyAccessMutation,
    variables: {
      input: { eventSlug, surveySlug, personId },
    },
  });

  revalidatePath(`/${locale}/${eventSlug}/surveys/${surveySlug}/access`);
}

const revokeSurveyAccessMutation = graphql(`
  mutation RevokeSurveyAccess($input: SurveyAccessInput!) {
    revokeSurveyAccess(input: $input) {
      survey {
        slug
      }
    }
  }
`);

export async function revokeSurveyAccess(
  locale: string,
  eventSlug: string,
  surveySlug: string,
  personId: number,
  _formData: FormData,
) {
  await getClient().mutate({
    mutation: revokeSurveyAccessMutation,
    variables: {
      input: { eventSlug, surveySlug, personId },
    },
  });

  revalidatePath(`/${locale}/${eventSlug}/surveys/${surveySlug}/access`);
}

const searchGrantablePeopleQuery = graphql(`
  query SearchGrantablePeople(
    $eventSlug: String!
    $surveySlug: String!
    $search: String
  ) {
    event(slug: $eventSlug) {
      forms {
        survey(slug: $surveySlug, app: FORMS) {
          grantablePeople(search: $search) {
            id
            fullName
            email
            nick
          }
        }
      }
    }
  }
`);

export async function searchGrantablePeople(
  eventSlug: string,
  surveySlug: string,
  search: string,
) {
  const { data } = await getClient().query({
    query: searchGrantablePeopleQuery,
    variables: { eventSlug, surveySlug, search },
    fetchPolicy: "no-cache",
  });

  return data.event?.forms?.survey?.grantablePeople ?? [];
}
