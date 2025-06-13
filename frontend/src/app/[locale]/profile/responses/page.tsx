import { notFound } from "next/navigation";

import { graphql } from "@/__generated__";
import { getClient } from "@/apolloClient";
import { auth } from "@/auth";
import DimensionBadge from "@/components/dimensions/DimensionBadge";
import Messages from "@/components/errors/Messages";
import SignInRequired from "@/components/errors/SignInRequired";
import ProfileResponsesTable from "@/components/forms/ProfileResponsesTable";
import ViewContainer from "@/components/ViewContainer";
import ViewHeading from "@/components/ViewHeading";
import { getTranslations } from "@/translations";

graphql(`
  fragment ProfileResponsesTableRow on ProfileResponseType {
    id
    revisionCreatedAt
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
    success?: string;
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

  return (
    <ViewContainer>
      <ViewHeading>{t.ownResponsesTitle}</ViewHeading>
      <Messages messages={t.messages} searchParams={searchParams} />

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
