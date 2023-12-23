import { notFound } from "next/navigation";

import { getTranslations } from "@/translations";
import { gql } from "@/__generated__";
import { getClient } from "@/apolloClient";
import { DataTable } from "@/components/DataTable";
import { EventFormResponsesQuery } from "@/__generated__/graphql";
import Link from "next/link";

const query = gql(`
  query EventFormResponses($eventSlug:String!, $surveySlug:String!, $locale:String) {
    event(slug: $eventSlug) {
      name

      forms {
        survey(slug: $surveySlug) {
          title(lang: $locale)

          responses {
            id
            createdAt
            language
            values
          }
        }
      }
    }
  }
`);

// TODO help :D
type ResponseRow = NonNullable<
  NonNullable<
    NonNullable<
      NonNullable<EventFormResponsesQuery["event"]>["forms"]
    >["survey"]
  >["responses"]
>[number];

interface EventFormResponsesProps {
  params: {
    locale: string;
    eventSlug: string;
    surveySlug: string;
  };
}

export async function generateMetadata({ params }: EventFormResponsesProps) {
  const { locale, eventSlug, surveySlug } = params;
  const t = getTranslations(locale);
  const { data } = await getClient().query({
    query,
    variables: { eventSlug, surveySlug, locale },
  });
  return {
    title: `${data.event?.name}: ${data.event?.forms?.survey?.title} – Kompassi`,
  };
}

export const revalidate = 0;

export default async function EventFormResponsesPage({
  params,
}: EventFormResponsesProps) {
  const { locale, eventSlug, surveySlug } = params;
  const t = getTranslations(locale).EventSurveyResponsesView;
  const { data } = await getClient().query({
    query,
    variables: { eventSlug, surveySlug, locale },
  });

  const columns = [
    {
      slug: "createdAt",
      title: t.columns.createdAt,
      getCell: (row: ResponseRow) => (
        <Link
          href={`/events/${eventSlug}/surveys/${surveySlug}/responses/${row.id}`}
        >
          {new Date(row.createdAt).toLocaleString()}
        </Link>
      ),
    },
    {
      slug: "language",
      title: t.columns.language,
    },
  ];

  if (!data.event?.forms?.survey) {
    notFound();
  }

  return (
    <main className="container mt-4">
      <h1>{data.event.forms.survey.title}</h1>
      <DataTable
        rows={data.event.forms.survey.responses || []}
        columns={columns}
      />
    </main>
  );
}
