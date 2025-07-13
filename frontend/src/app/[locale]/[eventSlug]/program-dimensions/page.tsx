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
import ProgramAdminView from "@/components/program/ProgramAdminView";
import getPageTitle from "@/helpers/getPageTitle";
import { getTranslations } from "@/translations";

const query = graphql(`
  query ProgramDimensionsList($eventSlug: String!, $locale: String!) {
    event(slug: $eventSlug) {
      name
      slug

      program {
        dimensions(publicOnly: false) {
          ...DimensionEditor
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

export async function generateMetadata({ params }: Props) {
  const { locale, eventSlug } = params;
  const translations = getTranslations(locale);

  // TODO encap
  const session = await auth();
  if (!session) {
    return translations.SignInRequired.metadata;
  }

  const t = translations.Survey;

  let resp;
  try {
    resp = await getClient().query({
      query,
      variables: { locale, eventSlug },
    });
  } catch (e) {
    console.error(await (e as any).networkError.response.json());
    throw e;
  }
  const data = resp.data;

  if (!data.event?.program?.dimensions) {
    notFound();
  }

  const title = getPageTitle({
    translations,
    event: data.event,
    viewTitle: t.attributes.dimensions,
  });

  return { title };
}

export default async function ProgramDimensionsPage({
  params,
  searchParams,
}: Props) {
  const { locale, eventSlug } = params;
  const translations = getTranslations(locale);

  // TODO encap
  const session = await auth();
  if (!session) {
    return <SignInRequired messages={translations.SignInRequired} />;
  }

  const t = translations.Survey;

  const { data } = await getClient().query({
    query,
    variables: { locale, eventSlug },
  });

  if (!data.event?.program?.dimensions) {
    notFound();
  }

  const dimensions = data.event.program.dimensions;

  return (
    <ProgramAdminView
      translations={translations}
      event={data.event}
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
    </ProgramAdminView>
  );
}
