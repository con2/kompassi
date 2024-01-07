import { notFound } from "next/navigation";

import { getClient } from "@/apolloClient";
import { getTranslations } from "@/translations";
import { gql } from "@/__generated__";
import ViewContainer from "@/components/ViewContainer";
import ViewHeading from "@/components/ViewHeading";

const query = gql(`
  query SurveyThankYouPageQuery($eventSlug:String!, $surveySlug:String!, $locale:String) {
    event(slug: $eventSlug) {
      name

      forms {
        survey(slug: $surveySlug) {
          form(lang: $locale) {
            title
            thankYouMessage
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
  };
}

export default async function SurveyPage({ params }: SurveyPageProps) {
  const { locale, eventSlug, surveySlug } = params;
  const t = getTranslations(locale).SurveyView;
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
  const { form } = survey;
  const { title, thankYouMessage } = form!;
  const message = thankYouMessage || t.thankYou.defaultMessage;

  return (
    <ViewContainer>
      <ViewHeading>{t.thankYou.title}</ViewHeading>
      <p>{message}</p>
    </ViewContainer>
  );
}
