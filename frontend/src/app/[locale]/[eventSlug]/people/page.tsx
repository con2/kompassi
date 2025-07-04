import Link from "next/link";
import { notFound } from "next/navigation";
import { ReactNode } from "react";
import { graphql } from "@/__generated__";
import { InvolvedPersonFragment } from "@/__generated__/graphql";
import { getClient } from "@/apolloClient";
import { auth } from "@/auth";
import { Column, DataTable } from "@/components/DataTable";
import { DimensionFilters } from "@/components/dimensions/DimensionFilters";
import { buildDimensionFilters } from "@/components/dimensions/helpers";
import SignInRequired from "@/components/errors/SignInRequired";
import ViewContainer from "@/components/ViewContainer";
import getPageTitle from "@/helpers/getPageTitle";
import { getTranslations } from "@/translations";

graphql(`
  fragment InvolvedPerson on ProfileWithInvolvementType {
    firstName
    lastName
    nick

    isActive

    involvements {
      id
      type
      title
      adminLink
      isActive
    }
  }
`);

const query = graphql(`
  query PeoplePage(
    $eventSlug: String!
    $filters: [DimensionFilterInput!]
    $locale: String
  ) {
    event(slug: $eventSlug) {
      slug
      name
      timezone

      involvement {
        dimensions(isListFilter: true) {
          ...DimensionFilter
        }

        people(filters: $filters) {
          ...InvolvedPerson
        }
      }
    }
  }
`);

interface Props {
  params: {
    locale: string;
    eventSlug: string;
  };
  searchParams: Record<string, string>;
}

export async function generateMetadata({ params, searchParams }: Props) {
  const { locale, eventSlug } = params;
  const translations = getTranslations(locale);
  const t = translations.Involvement;

  const session = await auth();
  if (!session) {
    return translations.SignInRequired.metadata;
  }

  const filters = buildDimensionFilters(searchParams);
  const { data } = await getClient().query({
    query,
    variables: { eventSlug, locale, filters },
  });

  if (!data.event?.involvement) {
    notFound();
  }

  const { event } = data;
  const title = getPageTitle({
    translations,
    event,
    viewTitle: t.listTitle,
  });
  return {
    title,
  };
}

function textMutedWhenInactive(
  this: Column<InvolvedPersonFragment>,
  row: InvolvedPersonFragment,
  children?: ReactNode,
) {
  const className = row.isActive
    ? this.className
    : `${this.className} text-muted`;

  return (
    <td scope={this.scope} className={className}>
      {children}
    </td>
  );
}

export default async function PeoplePage({ params, searchParams }: Props) {
  const { locale, eventSlug } = params;
  const translations = getTranslations(locale);
  const t = translations.Involvement;
  const profileT = translations.Profile;

  const session = await auth();
  if (!session) {
    return <SignInRequired messages={translations.SignInRequired} />;
  }

  const filters = buildDimensionFilters(searchParams);
  const { data } = await getClient().query({
    query,
    variables: { eventSlug, locale, filters },
  });

  if (!data.event?.involvement) {
    notFound();
  }

  const people = data.event.involvement.people;
  const dimensions = data.event.involvement.dimensions;

  const columns: Column<InvolvedPersonFragment>[] = [
    {
      slug: "lastName",
      title: profileT.attributes.lastName,
      getCellElement: textMutedWhenInactive,
    },
    {
      slug: "firstName",
      title: profileT.attributes.firstName,
      getCellElement: textMutedWhenInactive,
    },
    {
      slug: "nick",
      title: profileT.attributes.nick,
      getCellElement: textMutedWhenInactive,
    },
    {
      slug: "involvement",
      title: t.attributes.involvement.title,
      getCellContents: (row) => {
        return row.involvements.map((involvement) => {
          let className = "";
          if (!involvement.isActive) {
            className += " text-muted";
          }

          const active = involvement.isActive ? null : (
            <em> ({t.attributes.isActive.choices.inactive})</em>
          );

          const title = involvement.title ? (
            <>{involvement.title}</>
          ) : (
            <>
              <em>{t.attributes.title.missing}</em>
            </>
          );

          return (
            <div key={involvement.id} className={className}>
              <>
                {t.attributes.type.choices[involvement.type] ||
                  involvement.type}
                :{" "}
              </>
              {involvement.adminLink ? (
                <Link className="link-subtle" href={involvement.adminLink}>
                  {title}
                </Link>
              ) : (
                title
              )}
              {active}
            </div>
          );
        });
      },
    },
  ];

  const countInvolvements = people.reduce(
    (count, person) => count + person.involvements.length,
    0,
  );

  return (
    <ViewContainer>
      <DimensionFilters dimensions={dimensions} />
      <DataTable columns={columns} rows={people}>
        <tfoot>
          <tr>
            <td colSpan={columns.length}>
              {t.attributes.count(people.length, countInvolvements)}
            </td>
          </tr>
        </tfoot>
      </DataTable>
    </ViewContainer>
  );
}
