import Link from "next/link";
import { notFound } from "next/navigation";

import { graphql } from "@/__generated__";
import { ProfileResponsesTableRowFragment } from "@/__generated__/graphql";
import { getClient } from "@/apolloClient";
import { auth } from "@/auth";
import { Column, DataTable } from "@/components/DataTable";
import DimensionBadge from "@/components/dimensions/DimensionBadge";
import AlertNavigateOnClose from "@/components/errors/AlertNavigateOnClose";
import SignInRequired from "@/components/errors/SignInRequired";
import FormattedDateTime from "@/components/FormattedDateTime";
import ProfileResponsesTable from "@/components/forms/ProfileResponsesTable";
import ViewContainer from "@/components/ViewContainer";
import ViewHeading from "@/components/ViewHeading";
import { getTranslations } from "@/translations";

graphql(`
  fragment ProfileResponsesTableRow on ProfileResponseType {
    id
    createdAt
    canEdit(mode: OWNER)

    values(keyFieldsOnly: true)

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
      survey {
        slug
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
  searchParams: {
    editSuccess?: string;
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

export default async function OwnResponsesPage({
  params,
  searchParams,
}: Props) {
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

  const responses = data.profile.forms.responses;
  const editedResponse = searchParams.editSuccess
    ? responses.find((response) => response.id === searchParams.editSuccess)
    : null;

  return (
    <ViewContainer>
      <ViewHeading>{t.ownResponsesTitle}</ViewHeading>

      {editedResponse && (
        <AlertNavigateOnClose variant="success">
          {t.actions.editResponse.success(editedResponse.form.title)}
        </AlertNavigateOnClose>
      )}

      <ProfileResponsesTable
        messages={translations.Survey}
        responses={responses}
        locale={locale}
        footer={t.showingResponses(responses.length, responses.length)}
        extraColumns={[
          {
            slug: "formTitle",
            title: t.attributes.formTitle,
            getCellContents: (row) => (
              <>
                {row.form.title}
                <span className="ms-2">
                  {row.dimensions
                    .filter(
                      (dimension) =>
                        // Avoid duplication of program form title for program offers
                        !(
                          dimension.dimension.slug === "form" &&
                          dimension.value.slug === row.form.survey.slug
                        ),
                    )
                    .map((dimension) => (
                      <DimensionBadge
                        key={dimension.dimension.slug}
                        dimension={dimension}
                      />
                    ))}
                </span>
              </>
            ),
          },
        ]}
      />
    </ViewContainer>
  );
}
