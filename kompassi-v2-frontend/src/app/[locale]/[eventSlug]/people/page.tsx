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
import { decodeBoolean } from "@/helpers/decodeBoolean";

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
    $returnNone: Boolean = false
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

        people(filters: $filters, search: $search, returnNone: $returnNone) {
          ...InvolvedPerson
        }
      }
    }
  }
`);

interface Props {
  params: Promise<{
    locale: string;
    eventSlug: string;
  }>;
  searchParams: Promise<Record<string, string>>;
}

export async function generateMetadata(props: Props) {
  const searchParams = await props.searchParams;
  const params = await props.params;
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
    variables: { eventSlug, locale, filters, returnNone: true },
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

export default async function PeoplePage(props: Props) {
  const searchParams = await props.searchParams;
  const params = await props.params;
  const { locale, eventSlug } = params;
  const translations = getTranslations(locale);
  const t = translations.Involvement;
  const profileT = translations.Profile;

  const session = await auth();
  if (!session) {
    return <SignInRequired messages={translations.SignInRequired} />;
  }

  // XXX there should be a better way to handle this
  const {
    success: _success, // eslint-disable-line @typescript-eslint/no-unused-vars
    error: _error, // eslint-disable-line @typescript-eslint/no-unused-vars
    search = "",
    force = "false",
    ...filterSearchParams
  } = searchParams;
  const filters = buildDimensionFilters(filterSearchParams);
  const passedSearchParams = Object.fromEntries(
    Object.entries({ ...filterSearchParams, search, force }).filter(
      ([, value]) => !!value,
    ),
  );

  const showResults =
    decodeBoolean(force) || Object.entries(filters).length > 0 || !!search;

  const { data } = await getClient().query({
    query,
    variables: { eventSlug, locale, filters, search, returnNone: !showResults },
  });

  if (!data.event?.involvement) {
    notFound();
  }

  const { event } = data;
  const people = data.event.involvement.people;
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

          let link: ReactNode | null = null;
          if (involvement.adminLink) {
            if (involvement.adminLink.startsWith("/")) {
              link = (
                <Link className="link-subtle" href={involvement.adminLink}>
                  {title}
                </Link>
              );
            } else {
              link = (
                <a
                  className="link-subtle"
                  href={involvement.adminLink}
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  {title}
                </a>
              );
            }
          }

          return (
            <div key={involvement.id} className={className}>
              <>
                {t.attributes.type.choices[involvement.type] ||
                  involvement.type}
                :{" "}
              </>
              {link}
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

  function ForceLink({ children }: { children: React.ReactNode }) {
    const strongWithTheForce = new URLSearchParams({
      ...passedSearchParams,
      force: "strong",
    }).toString();
    return (
      <Link
        href={`/${event.slug}/people?${strongWithTheForce}`}
        className="link-subtle"
        prefetch={false}
      >
        {children}
      </Link>
    );
  }

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

      {showResults ? (
        <DataTable columns={columns} rows={people}>
          <tfoot>
            <tr>
              <td colSpan={columns.length}>
                {t.attributes.count(people.length, countInvolvements)}
              </td>
            </tr>
          </tfoot>
        </DataTable>
      ) : (
        <Alert variant="warning">{t.noFiltersApplied(ForceLink)}</Alert>
      )}
    </InvolvementAdminView>
  );
}
