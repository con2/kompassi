import { notFound } from "next/navigation";

import { SchemaForm } from "@/components/SchemaForm";
import { Field } from "@/components/SchemaForm/models";
import { getTranslations } from "@/translations";
import { gql } from "@/__generated__";
import { getClient } from "@/apolloClient";
import { submit } from "./actions";
import SubmitButton from "@/components/SchemaForm/SubmitButton";

const query = gql(`
  query SurveyPageQuery($eventSlug:String!, $surveySlug:String!, $locale:String) {
    event(slug: $eventSlug) {
      name

      survey(slug: $surveySlug) {
        form(lang: $locale) {
          title
          description
          fields
          layout
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
    title: `${data.event?.name}: ${data.event?.survey?.form?.title} – Kompassi`,
    description: data.event?.survey?.form?.description ?? "",
  };
}

export default async function SurveyPage({ params }: SurveyPageProps) {
  const { locale, eventSlug, surveySlug } = params;
  const t = getTranslations(locale).NewProgrammeView;
  const { data } = await getClient().query({
    query,
    variables: { eventSlug, surveySlug, locale },
  });
  const { event } = data;
  if (!event) {
    notFound();
  }
  const { survey } = event;
  if (!survey) {
    notFound();
  }
  const { form } = survey;
  const { title, description, layout } = form!;

  // TODO validate
  const fields: Field[] = form!.fields ?? [];

  return (
    <main className="container mt-4">
      <h1 className="mt-2 mb-4">
        {title}{" "}
        <span className="fs-5 text-muted">{t.forEvent(event.name)}</span>
      </h1>
      <p>{description}</p>
      <form action={submit.bind(null, locale, eventSlug, surveySlug)}>
        <SchemaForm fields={fields} layout={layout} />
        <SubmitButton layout={layout}>{t.submit}</SubmitButton>
      </form>
    </main>
  );
}
