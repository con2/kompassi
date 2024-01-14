import Link from "next/link";
import { notFound } from "next/navigation";

import { gql } from "@/__generated__";
import { SurveyResponseFragment } from "@/__generated__/graphql";
import { getClient } from "@/apolloClient";
import { auth } from "@/auth";
import { DataTable } from "@/components/DataTable";
import SignInRequired from "@/components/SignInRequired";
import ViewContainer from "@/components/ViewContainer";
import ViewHeading from "@/components/ViewHeading";
import { kompassiBaseUrl } from "@/config";
import { getTranslations } from "@/translations";

// this fragment is just to give a name to the type so that we can import it from generated
gql(`
  fragment SurveyResponse on LimitedResponseType {
    id
    createdAt
    language
    values
  }
`);

const query = gql(`
  query FormResponses($eventSlug:String!, $surveySlug:String!, $locale:String) {
    event(slug: $eventSlug) {
      name

      forms {
        survey(slug: $surveySlug) {
          title(lang: $locale)

          responses {
            ...SurveyResponse
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

  const t = translations.SurveyResponse;

  const { data } = await getClient().query({
    query,
    variables: { eventSlug, surveySlug, locale },
  });

  if (!data.event?.forms?.survey) {
    notFound();
  }

  return {
    title: `${data.event.name}: ${data.event.forms.survey.title} (${t.listTitle}) – Kompassi`,
  };
}

export const revalidate = 0;

export default async function FormResponsesPage({ params }: Props) {
  const { locale, eventSlug, surveySlug } = params;
  const translations = getTranslations(locale);
  const session = await auth();

  // TODO encap
  if (!session) {
    return <SignInRequired messages={translations.SignInRequired} />;
  }

  const { data } = await getClient().query({
    query,
    variables: { eventSlug, surveySlug, locale },
  });

  if (!data.event?.forms?.survey) {
    notFound();
  }

  const t = translations.SurveyResponse;
  const columns = [
    {
      slug: "createdAt",
      title: t.attributes.createdAt,
      getCell: (row: SurveyResponseFragment) => (
        <Link
          href={`/events/${eventSlug}/surveys/${surveySlug}/responses/${row.id}`}
        >
          {new Date(row.createdAt).toLocaleString()}
        </Link>
      ),
    },
    {
      slug: "language",
      title: t.attributes.language,
    },
  ];

  const excelUrl = `${kompassiBaseUrl}/events/${eventSlug}/surveys/${surveySlug}/responses.xlsx`;
  const responses = data.event.forms.survey.responses || [];

  return (
    <ViewContainer>
      <Link className="link-subtle" href={`/events/${eventSlug}/surveys`}>
        &lt; {t.actions.returnToSurveyList}
      </Link>

      <div className="d-flex align-items-middle">
        <ViewHeading>
          {t.listTitle}
          <ViewHeading.Sub>{data.event.forms.survey.title}</ViewHeading.Sub>
        </ViewHeading>
        <div className="ms-auto">
          <a className="btn btn-outline-primary" href={excelUrl}>
            {t.actions.downloadAsExcel}…
          </a>
        </div>
      </div>
      <DataTable rows={responses} columns={columns} />
      <p>{t.tableFooter(responses.length)}</p>
    </ViewContainer>
  );
}
