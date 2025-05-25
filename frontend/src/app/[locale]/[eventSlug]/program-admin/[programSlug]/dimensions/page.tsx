import Link from "next/link";
import { notFound } from "next/navigation";

import Card from "react-bootstrap/Card";
import CardBody from "react-bootstrap/CardBody";

import { updateProgramDimensions } from "./actions";
import { graphql } from "@/__generated__";
import { getClient } from "@/apolloClient";
import DimensionValueSelectionForm, {
  buildDimensionValueSelectionForm,
} from "@/components/dimensions/DimensionValueSelectionForm";
import { validateCachedDimensions } from "@/components/dimensions/models";
import ProgramAdminDetailView from "@/components/program/ProgramAdminDetailView";
import getPageTitle from "@/helpers/getPageTitle";
import { getTranslations } from "@/translations";

// TODO(Japsu) Deterministic order of dimensions & values
// See https://con2.slack.com/archives/C3ZGNGY48/p1718446605681339
const query = graphql(`
  query ProgramAdminDetailDimensionsQuery(
    $eventSlug: String!
    $programSlug: String!
    $locale: String
  ) {
    event(slug: $eventSlug) {
      slug
      name

      program {
        dimensions {
          ...DimensionRowGroup
        }

        program(slug: $programSlug) {
          slug
          title
          cachedDimensions
        }
      }
    }
  }
`);

interface Props {
  params: {
    locale: string;
    eventSlug: string;
    programSlug: string;
  };
}

export const revalidate = 0;

export async function generateMetadata({ params }: Props) {
  const { locale, eventSlug, programSlug } = params;
  const translations = getTranslations(locale);
  const { data, errors } = await getClient().query({
    query,
    variables: { eventSlug, programSlug, locale },
  });
  const title = getPageTitle({
    translations,
    event: data.event,
    viewTitle: translations.Program.adminDetailTabs.dimensions,
    subject: data?.event?.program?.program?.title,
  });
  return { title };
}

export default async function ProgramAdminDetailPage({ params }: Props) {
  const { locale, eventSlug, programSlug } = params;
  const translations = getTranslations(locale);
  const t = translations.Program;
  const surveyT = translations.Survey;
  const { data } = await getClient().query({
    query,
    variables: { eventSlug, programSlug, locale },
  });
  if (!data.event?.program?.program) {
    notFound();
  }

  const event = data.event;
  const program = data.event.program.program;
  const dimensions = data.event.program.dimensions;

  validateCachedDimensions(program.cachedDimensions);
  const { fields, values } = buildDimensionValueSelectionForm(
    dimensions,
    program.cachedDimensions,
  );

  return (
    <ProgramAdminDetailView
      event={event}
      program={program}
      translations={translations}
      active={"dimensions"}
    >
      <Card>
        <CardBody>
          <DimensionValueSelectionForm
            dimensions={dimensions}
            cachedDimensions={program.cachedDimensions}
            onChange={updateProgramDimensions.bind(
              null,
              locale,
              eventSlug,
              programSlug,
            )}
            translations={translations}
            technicalDimensions="readonly"
          />
          <p className="form-text mb-0">
            <Link
              className="link-subtle"
              href={`/${locale}/${eventSlug}/program-dimensions`}
              target="_blank"
            >
              {surveyT.actions.editDimensions}…
            </Link>
          </p>
        </CardBody>
      </Card>
    </ProgramAdminDetailView>
  );
}
