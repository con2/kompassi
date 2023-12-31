import Link from "next/link";
import { notFound } from "next/navigation";

import { getTranslations } from "@/translations";
import { gql } from "@/__generated__";
import { getClient } from "@/apolloClient";
import { DataTable } from "@/components/DataTable";
import { EventSurveyResponseFragment } from "@/__generated__/graphql";
import { SignInRequired } from "@/components/SignInRequired";

import { auth } from "@/auth";

// this fragment is just to give a name to the type so that we can import it from generated
gql(`
  fragment EventSurveyResponse on EventFormResponseType {
    id
    createdAt
    language
    values
  }
`);

const query = gql(`
  query EventFormResponses($eventSlug:String!, $surveySlug:String!, $locale:String) {
    event(slug: $eventSlug) {
      name

      forms {
        survey(slug: $surveySlug) {
          title(lang: $locale)

          responses {
            ...EventSurveyResponse
          }
        }
      }
    }
  }
`);

interface Props {
  params: {
    locale: string;
    eventSlug: string;
    surveySlug: string;
  };
}

export async function generateMetadata({ params }: Props) {
  const { locale, eventSlug, surveySlug } = params;
  const translations = getTranslations(locale);

  // TODO encap
  const session = await auth();
  if (!session) {
    return translations.SignInRequired.metadata;
  }

  const t = translations.EventSurveyResponsesView;

  const { data } = await getClient().query({
    query,
    variables: { eventSlug, surveySlug, locale },
  });

  return {
    title: `${data.event?.name}: ${data.event?.forms?.survey?.title} (${t.title}) – Kompassi`,
  };
}

export const revalidate = 0;

export default async function EventFormResponsesPage({ params }: Props) {
  const { locale, eventSlug, surveySlug } = params;
  const translations = getTranslations(locale);
  const session = await auth();

  // TODO encap
  if (!session) {
    return <SignInRequired translations={translations.SignInRequired} />;
  }

  const { data } = await getClient().query({
    query,
    variables: { eventSlug, surveySlug, locale },
  });

  const t = translations.EventSurveyResponsesView;
  const columns = [
    {
      slug: "createdAt",
      title: t.columns.createdAt,
      getCell: (row: EventSurveyResponseFragment) => (
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
      <h1 className="mt-2 mb-4">
        {t.title}{" "}
        <span className="fs-5 text-muted">{data.event.forms.survey.title}</span>
      </h1>
      <DataTable
        rows={data.event.forms.survey.responses || []}
        columns={columns}
      />
    </main>
  );
}
