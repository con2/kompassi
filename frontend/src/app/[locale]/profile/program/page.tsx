import { notFound } from "next/navigation";

import { graphql } from "@/__generated__";
import {
  ProfileProgramItemFragment,
  ProfileProgramOfferFragment,
} from "@/__generated__/graphql";
import { getClient } from "@/apolloClient";
import { auth } from "@/auth";
import { Column, DataTable } from "@/components/DataTable";
import DimensionBadge from "@/components/dimensions/DimensionBadge";
import SignInRequired from "@/components/errors/SignInRequired";
import ViewContainer from "@/components/ViewContainer";
import ViewHeading from "@/components/ViewHeading";
import getPageTitle from "@/helpers/getPageTitle";
import { getTranslations } from "@/translations";

graphql(`
  fragment ProfileProgramItem on FullProgramType {
    slug
    title
    event {
      slug
      name
    }
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
  }
`);

graphql(`
  fragment ProfileProgramOffer on FullResponseType {
    id
    createdAt
    values(keyFieldsOnly: true)

    form {
      event {
        slug
        name
      }
    }

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
  }
`);

const query = graphql(`
  query ProfileProgramItemList($locale: String!) {
    profile {
      program {
        programs(userRelation: HOSTING) {
          ...ProfileProgramItem
        }

        programOffers(filters: [{ dimension: "state", values: "new" }]) {
          ...ProfileProgramOffer
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
  const t = translations.Program;

  const title = getPageTitle({
    viewTitle: t.profile.title,
    translations,
  });

  return { title };
}

export const revalidate = 0;

export default async function ProfileProgramItemList({ params }: Props) {
  const { locale } = params;
  const translations = getTranslations(locale);
  const t = translations.Program;
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

  if (!data.profile?.program.programs) {
    notFound();
  }

  const programItemColumns: Column<ProfileProgramItemFragment>[] = [
    {
      slug: "event",
      title: t.attributes.event,
      getCellContents: (row) => row.event.name,
    },
    {
      slug: "title",
      title: t.attributes.title,
      getCellContents: (program) => (
        <>
          {program.title}
          <span className="ms-2">
            {program.dimensions?.map((dimension) => (
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

  const programOfferColumns: Column<ProfileProgramOfferFragment>[] = [
    {
      slug: "event",
      title: t.attributes.event,
      getCellContents: (row) => row.form.event.name,
    },
    {
      slug: "title",
      title: t.attributes.title,
      getCellContents: (program) => (
        <>
          {(program.values as Record<string, any>).title ?? ""}
          <span className="ms-2">
            {program.dimensions?.map((dimension) => (
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

  const programItems = data.profile.program.programs;
  const programOffers = data.profile.program.programOffers;

  return (
    <ViewContainer>
      <ViewHeading>{t.profile.title}</ViewHeading>
      {programItems.length > 0 && (
        <>
          <p>{t.profile.programItems.listTitle}:</p>
          <DataTable rows={programItems} columns={programItemColumns}>
            <tfoot>
              <tr>
                <td colSpan={programItemColumns.length}>
                  {t.profile.programItems.tableFooter(programItems.length)}
                </td>
              </tr>
            </tfoot>
          </DataTable>
        </>
      )}
      {programOffers.length > 0 && (
        <>
          <p>{t.profile.programOffers.listTitle}:</p>
          <DataTable rows={programOffers} columns={programOfferColumns}>
            <tfoot>
              <tr>
                <td colSpan={programOfferColumns.length}>
                  {t.profile.programOffers.tableFooter(programOffers.length)}
                </td>
              </tr>
            </tfoot>
          </DataTable>
        </>
      )}
      {programItems.length === 0 && programOffers.length === 0 && (
        <p>{t.profile.empty}</p>
      )}
    </ViewContainer>
  );
}
