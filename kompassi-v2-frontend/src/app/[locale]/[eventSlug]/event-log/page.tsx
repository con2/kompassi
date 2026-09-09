import {
  Column,
  DataTable,
  Dimension,
  DimensionFilters,
  FormattedDateTime,
  ModalButton,
  SignInRequired,
} from "@con2/components";
import { notFound } from "next/navigation";

import { graphql } from "@/__generated__";
import { InvolvementEventLogEntryFragment } from "@/__generated__/graphql";
import { getClient } from "@/apolloClient";
import { auth } from "@/auth";
import { buildDimensionFilters } from "@/components/dimensions/helpers";
import InvolvementAdminView from "@/components/involvement/InvolvementAdminView";
import getPageTitle from "@/helpers/getPageTitle";
import { getTranslations } from "@/translations";

graphql(`
  fragment InvolvementEventLogEntry on LimitedEventLogEntryType {
    id
    createdAt
    entryType
    message
    otherFields
    actor {
      fullName
    }
  }
`);

const query = graphql(`
  query InvolvementEventLog(
    $eventSlug: String!
    $filters: [DimensionFilterInput!]
  ) {
    event(slug: $eventSlug) {
      name
      slug

      involvement {
        eventLog(filters: $filters) {
          dimensions {
            slug
            values {
              slug
              title
            }
          }
          entries {
            ...InvolvementEventLogEntry
          }
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
  const params = await props.params;
  const { locale, eventSlug } = params;
  const translations = getTranslations(locale);
  const t = translations.EventLog;

  const session = await auth();
  if (!session) {
    return translations.SignInRequired.metadata;
  }

  const { data } = await getClient().query({
    query,
    variables: { eventSlug, filters: [] },
  });

  if (!data.event?.involvement) {
    notFound();
  }

  const title = getPageTitle({
    event: data.event,
    viewTitle: t.listTitle,
    translations,
  });

  return {
    title,
  };
}

export const revalidate = 0;

export default async function InvolvementEventLogPage(props: Props) {
  const searchParams = await props.searchParams;
  const params = await props.params;
  const { locale, eventSlug } = params;
  const translations = getTranslations(locale);
  const t = translations.EventLog;

  const session = await auth();
  if (!session) {
    return (
      <SignInRequired
        messages={translations.SignInRequired}
        providerId="kompassi"
        locale={locale}
      />
    );
  }

  const {
    success: _success, // eslint-disable-line @typescript-eslint/no-unused-vars
    error: _error, // eslint-disable-line @typescript-eslint/no-unused-vars
    ...filterSearchParams
  } = searchParams;
  const filters = buildDimensionFilters(filterSearchParams);

  const { data } = await getClient().query({
    query,
    variables: { eventSlug, filters },
  });

  if (!data.event?.involvement) {
    notFound();
  }

  const event = data.event;
  const { eventLog } = data.event.involvement;
  const entries = eventLog.entries;

  const dimensionTitles: Record<string, string> = {
    month: t.filters.month,
    type: t.filters.type,
    actor: t.filters.actor,
  };

  const dimensions: Dimension[] = eventLog.dimensions.map((dimension) => {
    let values = dimension.values;
    if (dimension.slug === "month") {
      values = [{ slug: "", title: t.filters.currentMonth }, ...values];
    } else if (dimension.slug === "actor") {
      values = [
        ...values,
        { slug: "system", title: t.attributes.actor.missing },
      ];
    }

    return {
      slug: dimension.slug,
      title: dimensionTitles[dimension.slug] ?? dimension.slug,
      values,
    };
  });

  const columns: Column<InvolvementEventLogEntryFragment>[] = [
    {
      slug: "createdAt",
      title: t.attributes.createdAt,
      getCellContents: (entry) => (
        <ModalButton
          title={entry.entryType}
          label={<FormattedDateTime value={entry.createdAt} locale={locale} />}
          className="btn btn-link link-subtle m-0 p-0"
          messages={t.actions.viewDetails.modalActions}
        >
          <dl>
            <dt>{t.attributes.createdAt}</dt>
            <dd>
              <FormattedDateTime value={entry.createdAt} locale={locale} />
            </dd>
            <dt>{t.attributes.actor.title}</dt>
            <dd>
              {entry.actor?.fullName ?? <em>{t.attributes.actor.missing}</em>}
            </dd>
            <dt>{t.attributes.entryType}</dt>
            <dd>{entry.entryType}</dd>
            <dt>{t.attributes.message}</dt>
            <dd>{entry.message}</dd>
          </dl>
          <pre>{JSON.stringify(entry.otherFields, null, 2)}</pre>
        </ModalButton>
      ),
    },
    {
      slug: "actor",
      title: t.attributes.actor.title,
      getCellContents: (entry) =>
        entry.actor?.fullName ?? <em>{t.attributes.actor.missing}</em>,
    },
    {
      slug: "entryType",
      title: t.attributes.entryType,
    },
    {
      slug: "message",
      title: t.attributes.message,
    },
  ];

  return (
    <InvolvementAdminView
      translations={translations}
      event={event}
      active="eventLog"
      searchParams={searchParams}
    >
      <DimensionFilters
        dimensions={dimensions}
        className="mt-1"
        locale={locale}
      />

      <DataTable columns={columns} rows={entries}>
        <tfoot>
          <tr>
            <td colSpan={columns.length}>
              {t.attributes.count(entries.length)}
            </td>
          </tr>
        </tfoot>
      </DataTable>
    </InvolvementAdminView>
  );
}
