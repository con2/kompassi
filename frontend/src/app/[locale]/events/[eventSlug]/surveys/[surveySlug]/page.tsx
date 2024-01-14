import { notFound } from "next/navigation";
import { ReactNode } from "react";

import { submit } from "./actions";
import { gql } from "@/__generated__";
import { getClient } from "@/apolloClient";
import { auth } from "@/auth";
import ParagraphsDangerousHtml from "@/components/helpers/ParagraphsDangerousHtml";
import { SchemaForm } from "@/components/SchemaForm";
import { Field, validateFields } from "@/components/SchemaForm/models";
import SubmitButton from "@/components/SchemaForm/SubmitButton";
import SignInRequired from "@/components/SignInRequired";
import ViewContainer from "@/components/ViewContainer";
import ViewHeading from "@/components/ViewHeading";
import { getTranslations } from "@/translations";

const query = gql(`
  query SurveyPageQuery($eventSlug:String!, $surveySlug:String!, $locale:String) {
    event(slug: $eventSlug) {
      name

      forms {
        survey(slug: $surveySlug) {
          loginRequired
          anonymity
          maxResponsesPerUser
          countResponsesByCurrentUser

          form(lang: $locale) {
            title
            description
            fields
            layout
          }
        }
      }
    }
  }
`);

interface SurveyPageProps {
  params: {
    locale: string;
    eventSlug: string;
    surveySlug: string;
  };
}

export const revalidate = 5;

export async function generateMetadata({ params }: SurveyPageProps) {
  const { locale, eventSlug, surveySlug } = params;
  const t = getTranslations(locale);
  const { data } = await getClient().query({
    query,
    variables: { eventSlug, surveySlug, locale },
  });
  return {
    title: `${data.event?.name}: ${data.event?.forms?.survey?.form?.title} – Kompassi`,
    description: data.event?.forms?.survey?.form?.description ?? "",
  };
}

export default async function SurveyPage({ params }: SurveyPageProps) {
  const { locale, eventSlug, surveySlug } = params;
  const translations = getTranslations(locale);
  const t = translations.Survey;
  const { data } = await getClient().query({
    query,
    variables: { eventSlug, surveySlug, locale },
  });
  const { event } = data;
  if (!event) {
    notFound();
  }
  const survey = event.forms?.survey;
  if (!survey) {
    notFound();
  }
  const {
    form,
    loginRequired,
    anonymity,
    maxResponsesPerUser,
    countResponsesByCurrentUser,
  } = survey;
  const { title, description, layout, fields } = form!;
  const anonymityMessages =
    translations.Survey.attributes.anonymity.secondPerson;

  if (loginRequired) {
    const session = await auth();
    if (!session) {
      return <SignInRequired messages={translations.SignInRequired} />;
    }
  }

  if (maxResponsesPerUser && countResponsesByCurrentUser) {
    if (countResponsesByCurrentUser >= maxResponsesPerUser) {
      return (
        <ViewContainer>
          <ViewHeading>{t.maxResponsesPerUserReached.title}</ViewHeading>
          <p>
            {t.maxResponsesPerUserReached.defaultMessage(
              maxResponsesPerUser,
              countResponsesByCurrentUser,
            )}
          </p>
        </ViewContainer>
      );
    }
  }

  validateFields(fields);

  return (
    <ViewContainer>
      <ViewHeading>
        {title}
        <ViewHeading.Sub>{t.forEvent(event.name)}</ViewHeading.Sub>
      </ViewHeading>
      <ParagraphsDangerousHtml html={description} />
      <p>
        <small>
          <strong>{anonymityMessages.title}: </strong>
          {anonymityMessages.choices[anonymity]}
        </small>
      </p>
      <form action={submit.bind(null, locale, eventSlug, surveySlug)}>
        <SchemaForm fields={fields} layout={layout} />
        <SubmitButton layout={layout}>{t.actions.submit}</SubmitButton>
      </form>
    </ViewContainer>
  );
}
