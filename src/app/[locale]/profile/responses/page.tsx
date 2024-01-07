import Link from "next/link";
import { notFound } from "next/navigation";

import { getTranslations } from "@/translations";
import { gql } from "@/__generated__";
import { getClient } from "@/apolloClient";
import { Column, DataTable } from "@/components/DataTable";
import { OwnResponseFragment } from "@/__generated__/graphql";
import { SignInRequired } from "@/components/SignInRequired";

import { auth } from "@/auth";
import ViewContainer from "@/components/ViewContainer";
import ViewHeading from "@/components/ViewHeading";

gql(`
  fragment OwnResponse on FullResponseType {
    id
    createdAt
    form {
      slug
      title
      event {
        slug
        name
      }
    }
  }
`);

const query = gql(`
  query OwnFormResponses {
    profile {
      forms {
        responses {
          ...OwnResponse
        }
      }
    }
  }
`);

interface Props {
  params: {
    locale: string;
  };
}

export async function generateMetadata({ params }: Props) {
  const { locale } = params;
  const translations = getTranslations(locale);
  const t = translations.SurveyResponse;

  return {
    title: `${t.ownResponses} – Kompassi`,
  };
}

export const revalidate = 0;

export default async function OwnResponsesPage({ params }: Props) {
  const { locale } = params;
  const translations = getTranslations(locale);
  const session = await auth();

  // TODO encap
  if (!session) {
    return <SignInRequired messages={translations.SignInRequired} />;
  }

  const { data } = await getClient().query({ query });

  if (!data.profile?.forms.responses) {
    notFound();
  }

  const t = translations.SurveyResponse;
  const columns: Column<OwnResponseFragment>[] = [
    {
      slug: "createdAt",
      title: t.attributes.createdAt,
      getCell: (row) => (
        <Link href={`/profile/responses/${row.id}`}>
          {new Date(row.createdAt).toLocaleString()}
        </Link>
      ),
    },
    {
      slug: "event",
      title: t.attributes.event,
      getCell: (row) => row.form.event.name,
    },
    {
      slug: "formTitle",
      title: t.attributes.formTitle,
      getCell: (row) => row.form.title,
    },
  ];

  const responses = data.profile.forms.responses;

  return (
    <ViewContainer>
      <ViewHeading>{t.ownResponses}</ViewHeading>
      <DataTable rows={responses} columns={columns} />
      <p>{t.tableFooter(responses.length)}</p>
    </ViewContainer>
  );
}
