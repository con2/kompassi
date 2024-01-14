import Link from "next/link";
import { notFound } from "next/navigation";

import { gql } from "@/__generated__";
import { SurveyResponseFragment } from "@/__generated__/graphql";
import { getClient } from "@/apolloClient";
import { auth } from "@/auth";
import { Column, DataTable } from "@/components/DataTable";
import { validateFields } from "@/components/SchemaForm/models";
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
    createdBy {
      displayName
    }
    language
    values(keyFieldsOnly: true)
  }
`);

const query = gql(`
  query FormResponses($eventSlug:String!, $surveySlug:String!, $locale:String) {
    event(slug: $eventSlug) {
      name

      forms {
        survey(slug: $surveySlug) {
          title(lang: $locale)
          anonymity

          fields(lang: $locale, keyFieldsOnly: true)

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
  const t = translations.SurveyResponse;
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

  const { anonymity } = data.event.forms.survey;
  const anonymityMessages =
    translations.Survey.attributes.anonymity.thirdPerson;

  const keyFields = data.event.forms.survey.fields;
  validateFields(keyFields);

  const columns: Column<SurveyResponseFragment>[] = [
    {
      slug: "createdAt",
      title: t.attributes.createdAt,
      getCell: (row) => (
        <Link
          href={`/events/${eventSlug}/surveys/${surveySlug}/responses/${row.id}`}
        >
          {new Date(row.createdAt).toLocaleString()}
        </Link>
      ),
    },
  ];

  if (anonymity === "NAME_AND_EMAIL") {
    columns.push({
      slug: "createdBy",
      title: t.attributes.createdBy,
      getCell: (row) => row.createdBy?.displayName || "",
    });
  }

  columns.push({
    slug: "language",
    title: t.attributes.language,
  });

  keyFields.forEach((keyField) => {
    columns.push({
      slug: `keyFields.${keyField.slug}`,
      title: keyField.summaryTitle ?? keyField.title ?? "",
      getCell(row) {
        // TODO as any
        const values: Record<string, any> = row.values as any;
        return values[keyField.slug];
      },
    });
  });

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

      <p>
        <small>
          <strong>{anonymityMessages.title}: </strong>
          {anonymityMessages.choices[anonymity]}
        </small>
      </p>

      <DataTable rows={responses} columns={columns} />
      <p>{t.tableFooter(responses.length)}</p>
    </ViewContainer>
  );
}
