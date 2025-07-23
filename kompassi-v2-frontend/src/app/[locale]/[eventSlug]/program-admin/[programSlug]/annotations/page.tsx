import { notFound } from "next/navigation";

import Card from "react-bootstrap/Card";
import CardBody from "react-bootstrap/CardBody";

import { updateProgramAnnotations } from "./actions";
import { graphql } from "@/__generated__";
import { getClient } from "@/apolloClient";
import AnnotationsForm from "@/components/annotations/AnnotationsForm";
import { validateCachedAnnotations } from "@/components/annotations/models";
import SubmitButton from "@/components/forms/SubmitButton";
import ProgramAdminDetailView from "@/components/program/ProgramAdminDetailView";
import getPageTitle from "@/helpers/getPageTitle";
import { getTranslations } from "@/translations";

// TODO(Japsu) Deterministic order of dimensions & values
// See https://con2.slack.com/archives/C3ZGNGY48/p1718446605681339
const query = graphql(`
  query ProgramAdminDetailAnnotationsQuery(
    $eventSlug: String!
    $programSlug: String!
    $locale: String
  ) {
    event(slug: $eventSlug) {
      slug
      name

      program {
        annotations(publicOnly: false) {
          ...AnnotationsFormAnnotation

          isApplicableToProgramItems
        }

        program(slug: $programSlug) {
          slug
          title
          cachedAnnotations(publicOnly: false)

          dimensions(publicOnly: false) {
            ...ProgramDimensionBadge
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
    programSlug: string;
  }>;
  searchParams: Promise<Record<string, string>>;
}

export const revalidate = 0;

export async function generateMetadata(props: Props) {
  const params = await props.params;
  const { locale, eventSlug, programSlug } = params;
  const translations = getTranslations(locale);
  const { data } = await getClient().query({
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

export default async function ProgramAdminDetailAnnotationsPage(props: Props) {
  const searchParams = await props.searchParams;
  const params = await props.params;
  const { locale, eventSlug, programSlug } = params;
  const translations = getTranslations(locale);
  const t = translations.Program;
  const { data } = await getClient().query({
    query,
    variables: { eventSlug, programSlug, locale },
  });
  if (!data.event?.program?.program) {
    notFound();
  }

  const event = data.event;
  const program = data.event.program.program;
  const schema = data.event.program.annotations;

  validateCachedAnnotations(schema, program.cachedAnnotations);

  const editableAnnotations = schema.filter(
    (ann) => !ann.isComputed && ann.isApplicableToProgramItems,
  );

  // need to tell updateProgramAnnotationsFromFormData which annotations
  // to look for in the formData
  const annotationSlugs = editableAnnotations.map((a) => a.slug);

  return (
    <ProgramAdminDetailView
      event={event}
      program={program}
      translations={translations}
      active={"annotations"}
      searchParams={searchParams}
      messages={t.messages}
    >
      <Card>
        <CardBody>
          <form
            action={updateProgramAnnotations.bind(
              null,
              locale,
              eventSlug,
              programSlug,
              annotationSlugs,
            )}
          >
            <AnnotationsForm
              schema={editableAnnotations}
              values={program.cachedAnnotations}
              messages={translations.SchemaForm}
            />
            <SubmitButton className="btn btn-primary mt-3">
              {translations.Common.standardActions.save}
            </SubmitButton>
          </form>
        </CardBody>
      </Card>
    </ProgramAdminDetailView>
  );
}
