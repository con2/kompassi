import Link from "next/link";
import { notFound } from "next/navigation";
import { ReactNode } from "react";
import { Alert } from "react-bootstrap";
import { graphql } from "@/__generated__";
import { InvolvedPersonFragment } from "@/__generated__/graphql";
import { getClient } from "@/apolloClient";
import { auth } from "@/auth";
import { Column, DataTable } from "@/components/DataTable";
import CachedDimensionBadges from "@/components/dimensions/CachedDimensionsBadges";
import { DimensionFilters } from "@/components/dimensions/DimensionFilters";
import { buildDimensionFilters } from "@/components/dimensions/helpers";
import { validateCachedDimensions } from "@/components/dimensions/models";
import SignInRequired from "@/components/errors/SignInRequired";
import InvolvementAdminView from "@/components/involvement/InvolvementAdminView";
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
      cachedDimensions
    }
  }
`);

const query = graphql(`
  query PeoplePage(
    $eventSlug: String!
    $filters: [DimensionFilterInput!]
    $locale: String
    $search: String
  ) {
    event(slug: $eventSlug) {
      slug
      name
      timezone

      involvement {
        dimensions(publicOnly: false) {
          ...DimensionFilter
          ...CachedDimensionsBadges
          ...DimensionValueSelect
        }

        people(filters: $filters, search: $search) {
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

function hideStatusActive(cachedDimensions: unknown) {
  validateCachedDimensions(cachedDimensions);
  const { state = [], ...rest } = cachedDimensions;
  return { ...rest, state: state.filter((s) => s !== "active") };
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
  const search = searchParams.search || "";
  const { data } = await getClient().query({
    query,
    variables: { eventSlug, locale, filters, search },
  });

  if (!data.event?.involvement) {
    notFound();
  }

  const { event } = data;
  let people = data.event.involvement.people;
  const dimensions = data.event.involvement.dimensions;
  const keyDimensions = dimensions.filter(
    (dimension) => dimension.isKeyDimension,
  );
  const listFilters = dimensions.filter((dimension) => dimension.isListFilter);

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
              <CachedDimensionBadges
                dimensions={keyDimensions}
                cachedDimensions={hideStatusActive(
                  involvement.cachedDimensions,
                )}
              />
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

  const isMessageShown = Object.entries(searchParams).length == 0;

  return (
    <InvolvementAdminView
      translations={translations}
      event={event}
      active="people"
      searchParams={searchParams}
    >
      <DimensionFilters
        dimensions={listFilters}
        className="mt-1"
        search={true}
        messages={t.filters}
      />

      {isMessageShown ? (
        <Alert variant="warning">
          {t.noFiltersApplied(people.length, countInvolvements)}
        </Alert>
      ) : (
        <DataTable columns={columns} rows={people}>
          <tfoot>
            <tr>
              <td colSpan={columns.length}>
                {t.attributes.count(people.length, countInvolvements)}
              </td>
            </tr>
          </tfoot>
        </DataTable>
      )}
    </InvolvementAdminView>
  );
}
