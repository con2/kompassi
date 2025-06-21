import Link from "next/link";
import { notFound } from "next/navigation";

import { ButtonGroup, CardText, CardTitle } from "react-bootstrap";
import Card from "react-bootstrap/Card";
import CardBody from "react-bootstrap/CardBody";

import { cancelProgramItem, updateProgramBasicInfo } from "./actions";
import { graphql } from "@/__generated__";
import { getClient } from "@/apolloClient";
import { Field } from "@/components/forms/models";
import { SchemaForm } from "@/components/forms/SchemaForm";
import SubmitButton from "@/components/forms/SubmitButton";
import ModalButton from "@/components/ModalButton";
import ProgramAdminDetailView from "@/components/program/ProgramAdminDetailView";
import getPageTitle from "@/helpers/getPageTitle";
import { getTranslations } from "@/translations";

const query = graphql(`
  query ProgramAdminDetailQuery(
    $eventSlug: String!
    $programSlug: String!
    $locale: String
  ) {
    event(slug: $eventSlug) {
      name
      slug
      timezone

      program {
        calendarExportLink

        program(slug: $programSlug) {
          slug
          title
          description
          cachedHosts

          canCancel
          canDelete

          programOffer {
            id
            values
          }

          links(lang: $locale) {
            type
            href
            title
          }

          annotations(isShownInDetail: true) {
            ...ProgramDetailAnnotation
          }

          dimensions(isShownInDetail: true) {
            dimension {
              slug
              title(lang: $locale)
            }
            value {
              slug
              title(lang: $locale)
            }
          }
          scheduleItems {
            slug
            subtitle
            location
            startTime
            endTime
          }
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
    viewTitle: translations.Program.singleTitle,
    subject: data?.event?.program?.program?.title,
  });
  const description = data?.event?.program?.program?.description;
  return { title, description };
}

export default async function ProgramAdminDetailPage({ params }: Props) {
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
  const { canCancel, canDelete } = data.event.program.program;

  const fields: Field[] = [
    {
      slug: "title",
      title: t.attributes.title,
      type: "SingleLineText",
    },
    {
      slug: "description",
      title: t.attributes.description,
      type: "MultiLineText",
      rows: 5,
    },
  ];

  const cancelProgramItemFields: Field[] = [
    {
      slug: "resolution",
      type: "SingleSelect",
      title: t.actions.cancel.attributes.resolution.title,
      required: true,
      choices: [
        {
          slug: "CANCEL",
          title: t.actions.cancel.attributes.resolution.choices.CANCEL,
          disabled: !canCancel,
        },
        {
          slug: "CANCEL_AND_HIDE",
          title: t.actions.cancel.attributes.resolution.choices.CANCEL_AND_HIDE,
          // disabled: !canCancel,
          disabled: true, // TODO: implement this
        },
        {
          slug: "DELETE",
          title: t.actions.cancel.attributes.resolution.choices.DELETE,
          disabled: !canDelete,
        },
      ],
    },
  ];

  return (
    <ProgramAdminDetailView
      event={event}
      program={program}
      translations={translations}
      active={"basicInfo"}
      actions={
        <ButtonGroup>
          <ModalButton
            className="btn btn-outline-danger"
            label={t.actions.cancel.label + "…"}
            title={t.actions.cancel.title}
            messages={t.actions.cancel.modalActions}
            disabled={!canCancel && !canDelete}
            action={cancelProgramItem.bind(
              null,
              locale,
              eventSlug,
              programSlug,
            )}
          >
            <p>{t.actions.cancel.message}</p>
            <SchemaForm
              fields={cancelProgramItemFields}
              messages={translations.SchemaForm}
            />
          </ModalButton>
        </ButtonGroup>
      }
    >
      <Card>
        <CardBody>
          {" "}
          <form
            action={updateProgramBasicInfo.bind(
              null,
              locale,
              event.slug,
              program.slug,
            )}
          >
            <SchemaForm
              fields={fields}
              values={program}
              messages={translations.SchemaForm}
            />
            <SubmitButton>{translations.Common.submit}</SubmitButton>
          </form>
        </CardBody>
      </Card>

      {program.programOffer && (
        <Card className="mt-4">
          <CardBody>
            <CardTitle>{t.attributes.programOffer.title}</CardTitle>
            <CardText>{t.attributes.programOffer.message}</CardText>
            <CardText>
              <Link
                className="link-subtle"
                href={`/${event.slug}/program-offers/${program.programOffer.id}`}
              >
                {(program.programOffer.values as any).title ||
                  program.programOffer.id}
              </Link>
            </CardText>
          </CardBody>
        </Card>
      )}
    </ProgramAdminDetailView>
  );
}
