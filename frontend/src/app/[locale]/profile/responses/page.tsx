import Link from "next/link";
import { notFound } from "next/navigation";

import { graphql } from "@/__generated__";
import { ProfileResponsesTableRowFragment } from "@/__generated__/graphql";
import { getClient } from "@/apolloClient";
import { auth } from "@/auth";
import { Column, DataTable } from "@/components/DataTable";
import DimensionBadge from "@/components/dimensions/DimensionBadge";
import SignInRequired from "@/components/errors/SignInRequired";
import FormattedDateTime from "@/components/FormattedDateTime";
import ViewContainer from "@/components/ViewContainer";
import ViewHeading from "@/components/ViewHeading";
import { getTranslations } from "@/translations";

graphql(`
  fragment ProfileResponsesTableRow on ProfileResponseType {
    id
    createdAt
    dimensions(keyDimensionsOnly: true) {
      dimension {
        slug
        title(lang: $locale)
      }

      value {
        slug
        title(lang: $locale)
        color
      }
    }
    form {
      title
      event {
        slug
        name
      }
    }
  }
`);

const query = graphql(`
  query OwnFormResponses($locale: String!) {
    profile {
      forms {
        responses {
          ...ProfileResponsesTableRow
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
  const t = translations.Survey;

  return {
    title: `${t.ownResponsesTitle} – Kompassi`,
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

  const { data } = await getClient().query({
    query,
    variables: {
      locale,
    },
  });

  if (!data.profile?.forms.responses) {
    notFound();
  }

  const t = translations.Survey;
  const columns: Column<ProfileResponsesTableRowFragment>[] = [
    {
      slug: "createdAt",
      title: t.attributes.createdAt,
      getCellContents: (row) => (
        <Link href={`/profile/responses/${row.id}`}>
          <FormattedDateTime
            value={row.createdAt}
            locale={locale}
            scope={row.form.event}
            session={session}
          />
        </Link>
      ),
    },
    {
      slug: "event",
      title: t.attributes.event,
      getCellContents: (row) => row.form.event.name,
    },
    {
      slug: "formTitle",
      title: t.attributes.formTitle,
      getCellContents: (row) => (
        <>
          {row.form.title}
          <span className="ms-2">
            {row.dimensions?.map((dimension) => (
              <DimensionBadge
                key={dimension.dimension.slug}
                dimension={dimension}
              />
            ))}
          </span>
        </>
      ),
    },
  ];

  const responses = data.profile.forms.responses;

  return (
    <ViewContainer>
      <ViewHeading>{t.ownResponsesTitle}</ViewHeading>
      <DataTable rows={responses} columns={columns} />
      <p>{t.showingResponses(responses.length, responses.length)}</p>
    </ViewContainer>
  );
}
