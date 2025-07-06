import { notFound } from "next/navigation";
import {
  createDimension,
  createDimensionValue,
  deleteDimension,
  deleteDimensionValue,
  reorderDimensions,
  reorderDimensionValues,
  updateDimension,
  updateDimensionValue,
} from "./actions";
import { graphql } from "@/__generated__";
import { getClient } from "@/apolloClient";
import { auth } from "@/auth";
import { DimensionEditor } from "@/components/dimensions/DimensionEditor";
import SignInRequired from "@/components/errors/SignInRequired";
import InvolvementAdminView from "@/components/involvement/InvolvementAdminView";
import { getTranslations } from "@/translations";

const query = graphql(`
  query InvolvementDimensionsList($eventSlug: String!, $locale: String!) {
    event(slug: $eventSlug) {
      name
      slug

      involvement {
        dimensions(publicOnly: false) {
          ...DimensionRowGroup
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

export const revalidate = 0;

export default async function PeoplePage({ params, searchParams }: Props) {
  const { locale, eventSlug } = params;
  const translations = getTranslations(locale);

  const session = await auth();
  if (!session) {
    return <SignInRequired messages={translations.SignInRequired} />;
  }

  const { data } = await getClient().query({
    query,
    variables: { eventSlug, locale },
  });

  if (!data.event?.involvement) {
    notFound();
  }

  const { event } = data;
  const dimensions = data.event.involvement.dimensions;

  return (
    <InvolvementAdminView
      translations={translations}
      event={event}
      active="dimensions"
      searchParams={searchParams}
    >
      <DimensionEditor
        dimensions={dimensions}
        translations={translations}
        onCreateDimension={createDimension.bind(null, locale, eventSlug)}
        onUpdateDimension={updateDimension.bind(null, locale, eventSlug)}
        onDeleteDimension={deleteDimension.bind(null, locale, eventSlug)}
        onReorderDimensions={reorderDimensions.bind(null, locale, eventSlug)}
        onCreateDimensionValue={createDimensionValue.bind(
          null,
          locale,
          eventSlug,
        )}
        onUpdateDimensionValue={updateDimensionValue.bind(
          null,
          locale,
          eventSlug,
        )}
        onDeleteDimensionValue={deleteDimensionValue.bind(
          null,
          locale,
          eventSlug,
        )}
        onReorderDimensionValues={reorderDimensionValues.bind(
          null,
          locale,
          eventSlug,
        )}
      />
    </InvolvementAdminView>
  );
}
